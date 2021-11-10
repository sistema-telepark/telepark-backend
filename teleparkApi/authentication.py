from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from .permission import IsSuperuser
from .helpers import check_attributes
from .static import HTTP_METHOD
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import json


@api_view([HTTP_METHOD.POST])
def auth_view(request):
    if(request.method != HTTP_METHOD.POST):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if (not check_attributes(request.POST, ['user', 'password'])):
        return Response('Datos incompletos', status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=request.POST['user'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if (not check_password(request.POST['password'], user.password)):
        return Response('Los datos ingresados son invalidos', status=status.HTTP_401_UNAUTHORIZED)

    if (not user.is_active):
        return Response('El usuario está deshabilitado', status=status.HTTP_401_UNAUTHORIZED)

    token = RefreshToken.for_user(user)

    return Response({'access_token': str(token.access_token), 'refresh_token': str(token)})


@api_view([HTTP_METHOD.POST])
@permission_classes([IsSuperuser])
def create_user(request):
    if(not request.user.is_superuser):
        return Response('No posee los permisos requeridos', status.HTTP_401_UNAUTHORIZED)

    body = json.loads(request.body.decode('utf-8'))
    if (request.method != HTTP_METHOD.POST):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if (not check_attributes(body, ['user', 'password', 'is_superuser', 'is_staff', 'email'])):
        return Response('Datos incompletos', status=status.HTTP_400_BAD_REQUEST)

    if (User.objects.filter(username=body['user']).exists()):
        return Response('El usuario ya existe', status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=body['user'], password=body['password'],
                             is_superuser=body['is_superuser'], is_staff=body['is_staff'], email=body['email'])

    return Response('OK', status=status.HTTP_201_CREATED)
