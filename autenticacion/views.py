from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView

from core.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundException,
    PermissionDeniedError,
    ConflictError,
)
from core.permission import IsSuperuser
from autenticacion.serializers import (
    LoginSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    RoleChangeSerializer,
    UserListOutputSerializer,
)
from autenticacion.services import UsuarioService


@extend_schema_view(post=extend_schema(tags=['autenticacion']))
class TokenRefreshViewWrapper(TokenRefreshView):
    """Wrapper de TokenRefreshView que agrega el tag 'usuario' en Swagger."""
    pass


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
    try:
        result = UsuarioService.autenticar(serializer.validated_data)
    except AuthenticationError as e:
        return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(result, status=status.HTTP_200_OK)


@extend_schema(
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
)
@api_view(['POST'])
@permission_classes([IsSuperuser])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        result = UsuarioService.crear(serializer.validated_data)
    except ValidationError as e:
        if e.args and isinstance(e.args[0], dict):
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)


@extend_schema(
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
        400: OpenApiResponse(description="Datos inválidos o usuario no encontrado"),
    },
)
@api_view(['PUT'])
@permission_classes([IsSuperuser])
def update_user(request):
    serializer = UpdateUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        result = UsuarioService.actualizar(serializer.validated_data)
    except ValidationError as e:
        if e.args and isinstance(e.args[0], dict):
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)


@extend_schema(
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
)
@api_view(['GET'])
@permission_classes([IsSuperuser])
def get_users(request):
    filters = {}
    for param in ('is_superuser', 'is_active', 'search'):
        value = request.query_params.get(param)
        if value is not None:
            if param in ('is_superuser', 'is_active'):
                filters[param] = value.lower() == 'true'
            else:
                filters[param] = value

    users = UsuarioService.listar(filters=filters)
    paginator = PageNumberPagination()
    paginator.page_size = 50
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserListOutputSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@extend_schema(
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
)
@api_view(['PUT'])
@permission_classes([IsSuperuser])
def change_user_role(request, username):
    serializer = RoleChangeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        result = UsuarioService.cambiar_rol(
            actor_user=request.user,
            target_username=username,
            is_superuser=serializer.validated_data['is_superuser'],
        )
    except NotFoundException as e:
        return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except PermissionDeniedError as e:
        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
    except ConflictError as e:
        return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)
    return Response(result, status=status.HTTP_200_OK)
