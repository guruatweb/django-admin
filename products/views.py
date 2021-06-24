from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from DRFNEW.pagination import CustomPagination
from products.models import Products
from products.serializers import ProductSerializer
from users.authentication import JWTAuthentication


class ProductGenericView(generics.GenericAPIView, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                         mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(request, pk).data
            })

        return self.list(request)

    def post(self, request):
        return Response({
            'data': self.create(request).data
        })

    def delete(self, request, pk=None):
        return self.destroy(request, pk)

    def put(self, request, pk=None):
        return Response({
            'data': self.partial_update(request, pk).data
        })


class FileUploadAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post(self, request):
        file = request.FILES['image']
        file_name=default_storage.save(file.name,file)
        url=default_storage.url(file_name)

        return Response({
            'url' : 'http://127.0.0.1:8000/api' + url
        })
