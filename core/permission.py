from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    message = 'Not allowed.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
