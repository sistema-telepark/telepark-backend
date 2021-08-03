from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

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