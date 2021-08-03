from rest_framework import status
from rest_framework.response import Response
from functools import wraps

def has_permission(allowed=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            return func(request, *args, **kwargs) if request.user.has_perm(*allowed) else Response(status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return decorator