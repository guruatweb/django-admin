from django.urls import path
from .views import (
    hello,
    register,
    login,
    AuthenticatedUser,
    logout,
    PermissionAPI,
    RoleViewSet,
    UsersGenericView,
    ProfileInfoAPIView,
    ProfilePasswordAPIView,
    UserpartialUpdate,
)

urlpatterns = [
    path('hello', hello),
    path('user', AuthenticatedUser.as_view()),
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('Permissions', PermissionAPI.as_view()),
    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('roles/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete':'destroy'
    })),

    path('user_update/<str:pk>', UserpartialUpdate.as_view({'put': 'update'})),

    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfileInfoAPIView.as_view()),
    path('users', UsersGenericView.as_view()),
    path('users/<str:pk>', UsersGenericView.as_view()),
]
