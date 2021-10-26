from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import json

@api_view(['POST'])
def auth_view(request):
    if(request.method != 'POST'):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if ('user' not in request.POST or 'password' not in request.POST):
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
    
    return Response({ 'access_token': str(token.access_token), 'refresh_token': str(token) })

@api_view(['POST'])
def create_user(request):
    body = json.loads(request.body.decode('utf-8'))
    if (request.method != 'POST'):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if ('user' not in body or 'password' not in body or 'is_superuser' not in body or 'is_staff' not in body or 'email' not in body):
        return Response('Datos incompletos', status=status.HTTP_400_BAD_REQUEST)

    if (User.objects.filter(username=body['user']).exists()):
        return Response('El usuario ya existe', status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=body['user'], password=body['password'], is_superuser=body['is_superuser'], is_staff=body['is_staff'], email=body['email'])

    return Response('OK', status=status.HTTP_201_CREATED)
