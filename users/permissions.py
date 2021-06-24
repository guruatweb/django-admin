from rest_framework import permissions

from .serializers import UserSerializers


class ViewPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        data = UserSerializers(request.user).data

        view_access=any(p['name'] == 'view_'+view.permission_object for p in data['role']['permission'])
        edit_access=any(p['name'] == 'edit_'+view.permission_object for p in data['role']['permission'])

        if request.method == 'GET' :
            return view_access or edit_access

        return edit_access

