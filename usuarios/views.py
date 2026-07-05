from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from core.permission import IsSuperuser
from usuarios.serializers import (
    LoginSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    UserListOutputSerializer,
)
from usuarios.services import UsuarioService


@extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Login exitoso — retorna JWT access/refresh y datos del usuario",
            response={
                "type": "object",
                "properties": {
                    "access": {"type": "string", "description": "JWT access token"},
                    "refresh": {"type": "string", "description": "JWT refresh token"},
                    "is_superuser": {"type": "boolean"},
                    "username": {"type": "string"},
                    "name": {"type": "string", "description": "Nombre completo del usuario"},
                },
            },
        ),
        401: OpenApiResponse(description="Credenciales inválidas o usuario inactivo"),
    },
)
@api_view(['POST'])
def auth_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = UsuarioService.autenticar(serializer.validated_data)
    return Response(result, status=status.HTTP_200_OK)


@extend_schema(
    request=CreateUserSerializer,
    responses={
        201: OpenApiResponse(
            description="Usuario creado exitosamente",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
            },
        ),
        400: OpenApiResponse(description="Datos inválidos o usuario ya existe"),
    },
)
@api_view(['POST'])
@permission_classes([IsSuperuser])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = UsuarioService.crear(serializer.validated_data)
    return Response(result, status=status.HTTP_201_CREATED)


@extend_schema(
    request=UpdateUserSerializer,
    responses={
        200: OpenApiResponse(
            description="Usuario actualizado exitosamente",
            response={
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                },
            },
        ),
        400: OpenApiResponse(description="Datos inválidos o usuario no encontrado"),
    },
)
@api_view(['PUT'])
@permission_classes([IsSuperuser])
def update_user(request):
    serializer = UpdateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    result = UsuarioService.actualizar(serializer.validated_data)
    return Response(result, status=status.HTTP_200_OK)


@extend_schema(
    responses={
        200: OpenApiResponse(
            description="Lista de usuarios del sistema",
            response={
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "first_name": {"type": "string"},
                                "last_name": {"type": "string"},
                                "is_superuser": {"type": "boolean"},
                                "is_active": {"type": "boolean"},
                            },
                        },
                    },
                },
            },
        ),
    },
)
@api_view(['GET'])
@permission_classes([IsSuperuser])
def get_users(request):
    users = UsuarioService.listar()
    serializer = UserListOutputSerializer(users, many=True)
    return Response({'data': serializer.data}, status=status.HTTP_200_OK)
