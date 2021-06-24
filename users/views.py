from rest_framework import exceptions, viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DRFNEW.pagination import CustomPagination
from .authentication import generate_access_token, JWTAuthentication
from .models import User, Permission, Role

# Create your views here.
from .serializers import UserSerializers, PermisionSerializers, RoleSerializers

from .permissions import ViewPermissions


@api_view(['POST'])
def hello(request):
    return Response('hello guru here')


@api_view(['POST'])
def register(request):
    data = request.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Password Does not match')
    serializer = UserSerializers(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password1 = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('user not found')

    if not user.check_password(password1):
        raise exceptions.AuthenticationFailed('password does not match')

    responce = Response()
    responce["Access-Control-Allow-Credentials"] = 'true'

    token = generate_access_token(user)

    responce.set_cookie(key='jwt', value=token, httponly=True)
    responce.data = {
        'jwt': token
    }

    return responce


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializers(request.user).data
        data['permission'] = [p['name'] for p in data['role']['permission']]
        return Response({
            'data': data
        })


@api_view(['POST'])
def logout(request):
    responce = Response()
    responce.delete_cookie(key='jwt')

    responce.data = {
        'message': 'success'
    }

    return responce


class PermissionAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermisionSerializers(Permission.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'roles'

    def list(self, request):
        serializer = RoleSerializers(Role.objects.all(), many=True)
        return Response({
            'data': serializer.data
        })

    def create(self, request):
        serializer = RoleSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializers(role)

        return Response({
            'data': serializer.data
        })

    def update(self, request, pk=None):
        role = Role.objects.get(id=pk)
        serializer = RoleSerializers(instance=role, data=request.data)
        serializer.is_valid()
        serializer.save()

        return Response({
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        role.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserpartialUpdate(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = UserSerializers(instance=user, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)


class UsersGenericView(generics.GenericAPIView, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                       mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permission_object = 'users'
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        request.data.update({
            'password': 1234,
            'role': request.data['role_id']
        })
        return Response({
            'data': self.create(request).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def put(self, request, pk=None):
        if request.data['role_id']:
            request.data.update({
                'role': request.data['role_id']
            })

        return Response({
            'data': self.partial_update(request, pk).data
        })


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data
        })


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user

        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('password do not match')

        serializer = UserSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data
        })
