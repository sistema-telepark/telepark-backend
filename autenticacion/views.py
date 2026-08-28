from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from core.permission import IsSuperuser
from autenticacion.serializers import (
    LoginSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    RoleChangeSerializer,
    UserListOutputSerializer,
)
from autenticacion.helpers import (
    autenticar,
    crear_usuario,
    actualizar_usuario,
    listar_usuarios,
    cambiar_rol,
    obtener_usuario_por_id,
    eliminar_usuario,
)


@extend_schema(
    tags=['autenticacion'],
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
    result = autenticar(serializer.validated_data)
    return Response(result, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        operation_id='usuarios_list',
        tags=['autenticacion'],
        parameters=[
            OpenApiParameter(
                name="search",
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Búsqueda por username, nombre, apellido o email",
            ),
            OpenApiParameter(
                name="is_superuser",
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrar por administrador",
            ),
            OpenApiParameter(
                name="is_active",
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtrar por activo/inactivo",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Lista paginada de usuarios del sistema",
                response={
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "next": {"type": "string", "nullable": True},
                        "previous": {"type": "string", "nullable": True},
                        "results": {
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
    ),
    post=extend_schema(
        tags=['autenticacion'],
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
    ),
)
@api_view(['GET', 'POST'])
@permission_classes([IsSuperuser])
def usuarios_list(request):
    if request.method == 'GET':
        filters = {}
        for param in ('is_superuser', 'is_active', 'search'):
            value = request.query_params.get(param)
            if value is not None:
                if param in ('is_superuser', 'is_active'):
                    filters[param] = value.lower() == 'true'
                else:
                    filters[param] = value

        users = listar_usuarios(filters=filters)
        paginator = PageNumberPagination()
        paginator.page_size = 50
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserListOutputSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = crear_usuario(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        operation_id='usuarios_detail',
        tags=['autenticacion'],
        responses={
            200: OpenApiResponse(
                description="Detalle de un usuario del sistema",
                response={
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "first_name": {"type": "string"},
                        "last_name": {"type": "string"},
                        "email": {"type": "string"},
                        "is_superuser": {"type": "boolean"},
                        "is_active": {"type": "boolean"},
                    },
                },
            ),
            404: OpenApiResponse(description="Usuario no encontrado"),
        },
    ),
    put=extend_schema(
        tags=['autenticacion'],
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
            400: OpenApiResponse(description="Datos inválidos"),
            404: OpenApiResponse(description="Usuario no encontrado"),
        },
    ),
    patch=extend_schema(
        tags=['autenticacion'],
        request=RoleChangeSerializer,
        responses={
            200: OpenApiResponse(
                description="Rol actualizado exitosamente",
                response={
                    "type": "object",
                    "properties": {
                        "message": {"type": "string"},
                        "username": {"type": "string"},
                        "is_superuser": {"type": "boolean"},
                    },
                },
            ),
            400: OpenApiResponse(description="Error de validación — is_superuser requerido o tipo inválido"),
            403: OpenApiResponse(description="No autorizado — no eres superusuario o intentas modificar tu propio rol"),
            404: OpenApiResponse(description="Usuario no encontrado"),
            409: OpenApiResponse(description="Conflicto — no puedes degradar al último administrador"),
        },
    ),
    delete=extend_schema(
        tags=['autenticacion'],
        responses={
            204: OpenApiResponse(description="Usuario eliminado exitosamente"),
            403: OpenApiResponse(description="No puedes eliminar tu propio usuario"),
            404: OpenApiResponse(description="Usuario no encontrado"),
        },
    ),
)
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsSuperuser])
def usuarios_detail(request, idusuario):
    if request.method == 'GET':
        user = obtener_usuario_por_id(idusuario)
        serializer = UserListOutputSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = actualizar_usuario(
            serializer.validated_data,
            user_id=idusuario,
        )
        return Response(result, status=status.HTTP_200_OK)

    elif request.method == 'PATCH':
        serializer = RoleChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = cambiar_rol(
            actor_user=request.user,
            target_id=idusuario,
            is_superuser=serializer.validated_data['is_superuser'],
        )
        return Response(result, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        if request.user.id == idusuario:
            raise PermissionError('No puedes eliminar tu propio usuario')
        eliminar_usuario(idusuario)
        return Response(status=status.HTTP_204_NO_CONTENT)
