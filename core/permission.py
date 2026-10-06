from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    message = 'Solo un superusuario puede realizar esta acción.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class AdminOrReadOnly(permissions.BasePermission):
    message = 'Solo un administrador puede modificar este recurso.'

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_superuser)


class AdminOnlyForDelete(permissions.BasePermission):
    message = 'Solo un administrador puede eliminar este recurso.'

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method == 'DELETE':
            return bool(request.user.is_superuser)
        return True
