"""Helpers modulares para autenticación y gestión de usuarios.

Reemplaza a UsuarioService (clase) con funciones independientes,
preservando toda la lógica de negocio original.
"""
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken


def autenticar(data):
    """Autentica un usuario con username/password y retorna JWT tokens."""
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError('Credenciales inválidas')

    if not check_password(password, user.password):
        raise ValueError('Credenciales inválidas')

    if not user.is_active:
        raise ValueError('El usuario está deshabilitado')

    token = RefreshToken.for_user(user)

    return {
        'access': str(token.access_token),
        'refresh': str(token),
        'is_superuser': user.is_superuser,
        'username': user.username,
        'name': user.get_full_name(),
    }


def crear_usuario(data):
    """Crea un nuevo usuario con validaciones."""
    username = data.get('user')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        raise ValueError('El usuario ya existe')

    if email and User.objects.filter(email=email).exists():
        raise ValueError({'email': 'El email ya está registrado'})

    password = data.get('password')
    try:
        validate_password(password)
    except DjangoValidationError as e:
        raise ValueError({'password': list(e.messages)})

    User.objects.create_user(
        username=username,
        email=email,
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        password=password,
        is_superuser=data.get('is_superuser', False),
        is_staff=data.get('is_staff', False),
        is_active=data.get('is_active', True),
    )

    return {'message': 'Usuario creado correctamente'}


def actualizar_usuario(data, user_id=None):
    """Actualiza un usuario existente por su ID."""
    if user_id is None:
        user_id = data.get('user')

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise ValueError('Usuario no encontrado')

    if 'email' in data:
        new_email = data['email']
        if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
            raise ValueError({'email': 'El email ya está registrado'})
        user.email = new_email

    if 'password' in data:
        password = data['password']
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValueError({'password': list(e.messages)})
        user.set_password(password)

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'is_active' in data:
        user.is_active = data['is_active']
    if 'is_superuser' in data:
        user.is_superuser = data['is_superuser']

    user.save()

    return {'message': 'Usuario actualizado correctamente'}


def listar_usuarios(filters=None):
    """Lista usuarios con filtros opcionales."""
    qs = User.objects.all().order_by('id')
    if filters:
        if 'is_superuser' in filters:
            qs = qs.filter(is_superuser=filters['is_superuser'])
        if 'is_active' in filters:
            qs = qs.filter(is_active=filters['is_active'])
        if 'search' in filters:
            search = filters['search']
            qs = qs.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
    return qs


def cambiar_rol(actor_user, target_id, is_superuser):
    """Cambia el rol de un usuario (admin/terapeuta)."""
    try:
        target = User.objects.get(pk=target_id)
    except User.DoesNotExist:
        raise LookupError('Usuario no encontrado')

    if actor_user == target:
        raise PermissionError('No puedes modificar tu propio rol')

    if not is_superuser:
        admin_count = User.objects.filter(is_superuser=True, is_active=True).count()
        if admin_count == 1 and target.is_superuser:
            raise ValueError('No puedes degradar al último administrador del sistema')

    target.is_superuser = is_superuser
    target.is_staff = is_superuser

    target.save()

    return {
        'message': f'Rol actualizado a {"admin" if is_superuser else "terapeuta"}',
        'username': target.username,
        'is_superuser': is_superuser,
    }


def obtener_usuario_por_id(user_id):
    """Obtiene un usuario por su ID."""
    try:
        return User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise LookupError('Usuario no encontrado')


def eliminar_usuario(user_id):
    """Elimina un usuario por su ID."""
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise LookupError('Usuario no encontrado')
    user.delete()
    return {'message': 'Usuario eliminado correctamente'}
