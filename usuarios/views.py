from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from core.permission import IsSuperuser
from core.helpers import check_attributes
from core.static import HTTP_METHOD
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import json


@api_view([HTTP_METHOD.POST])
def auth_view(request):
    body = json.loads(request.body.decode('utf-8'))
    if(request.method != HTTP_METHOD.POST):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    if (not check_attributes(body, ['username', 'password'])):
        return Response('Datos incompletos', status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=body['username'])
    except User.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if (not check_password(body['password'], user.password)):
        return Response('Los datos ingresados son invalidos', status=status.HTTP_401_UNAUTHORIZED)

    if (not user.is_active):
        return Response('El usuario está deshabilitado', status=status.HTTP_401_UNAUTHORIZED)

    token = RefreshToken.for_user(user)

    return Response({'access': str(token.access_token), 'refresh': str(token), 'is_superuser': user.is_superuser, 'username': user.username, 'name': user.get_full_name()}, status=status.HTTP_200_OK)


@api_view([HTTP_METHOD.POST])
@permission_classes([IsSuperuser])
def create_user(request):
    if(not request.user.is_superuser):
        return Response('No posee los permisos requeridos', status.HTTP_401_UNAUTHORIZED)

    body = json.loads(request.body.decode('utf-8'))
    if (request.method != HTTP_METHOD.POST):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if (not check_attributes(body, ['user', 'first_name', 'last_name', 'password', 'is_superuser', 'is_staff', 'is_active'])):
        return Response('Datos incompletos', status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=body['user']).exists():
        return Response('El usuario ya existe', status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=body['user'],
        first_name=body['first_name'],
        last_name=body['last_name'],
        password=body['password'],
        is_superuser=body['is_superuser'],
        is_staff=body['is_staff'],
        is_active=body['is_active'],
    )
    return Response({'messagge': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)


@api_view([HTTP_METHOD.PUT])
@permission_classes([IsSuperuser])
def update_user(request):
    if(not request.user.is_superuser):
        return Response('No posee los permisos requeridos', status.HTTP_401_UNAUTHORIZED)

    body = json.loads(request.body.decode('utf-8'))

    if (request.method != HTTP_METHOD.PUT):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if (not check_attributes(body, ['user'])):
        return Response('Datos incompletos', status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(username=body['user'])
    if 'password' in body:
        user.set_password(body['password'])
    if 'first_name' in body:
        user.first_name = body['first_name']
    if 'last_name' in body:
        user.last_name = body['last_name']
    if 'is_active' in body:
        user.is_active = body['is_active']
    if 'is_superuser' in body:
        user.is_superuser = body['is_superuser']
    if 'is_staff' in body:
        user.is_staff = body['is_staff']
    user.save()
    return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)


@api_view([HTTP_METHOD.GET])
@permission_classes([IsSuperuser])
def get_users(request):
    if(not request.user.is_superuser):
        return Response('No posee los permisos requeridos', status.HTTP_401_UNAUTHORIZED)

    users = User.objects.all().values('username', 'first_name', 'last_name', 'is_superuser', 'is_active')
    return Response({'data': list(users)}, status=status.HTTP_200_OK)
