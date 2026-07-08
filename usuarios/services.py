from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken

from core.exceptions import (
    AuthenticationError,
    ValidationError,
    NotFoundException,
    PermissionDeniedError,
    ConflictError,
)


class UsuarioService:
    """Lógica de negocio para autenticación y gestión de usuarios."""

    @staticmethod
    def autenticar(data):
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationError('Credenciales inválidas')

        if not check_password(password, user.password):
            raise AuthenticationError('Credenciales inválidas')

        if not user.is_active:
            raise AuthenticationError('El usuario está deshabilitado')

        token = RefreshToken.for_user(user)

        return {
            'access': str(token.access_token),
            'refresh': str(token),
            'is_superuser': user.is_superuser,
            'username': user.username,
            'name': user.get_full_name(),
        }

    @staticmethod
    def crear(data):
        username = data.get('user')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            raise ValidationError('El usuario ya existe')

        if email and User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'El email ya está registrado'})

        password = data.get('password')
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError({'password': list(e.messages)})

        User.objects.create_user(
            username=username,
            email=email,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=password,
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        return {'message': 'Usuario creado correctamente'}

    @staticmethod
    def actualizar(data):
        username = data.get('user')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('Usuario no encontrado')

        if 'email' in data:
            new_email = data['email']
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                raise ValidationError({'email': 'El email ya está registrado'})
            user.email = new_email

        if 'password' in data:
            password = data['password']
            try:
                validate_password(password)
            except DjangoValidationError as e:
                raise ValidationError({'password': list(e.messages)})
            user.set_password(password)

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']

        user.save()

        return {'message': 'Usuario actualizado correctamente'}

    @staticmethod
    def listar(filters=None):
        qs = User.objects.all()
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

    @staticmethod
    def cambiar_rol(actor_user, target_username, is_superuser):
        try:
            target = User.objects.get(username=target_username)
        except User.DoesNotExist:
            raise NotFoundException('Usuario no encontrado')

        if actor_user == target:
            raise PermissionDeniedError('No puedes modificar tu propio rol')

        if not is_superuser:
            admin_count = User.objects.filter(is_superuser=True, is_active=True).count()
            if admin_count == 1 and target.is_superuser:
                raise ConflictError('No puedes degradar al último administrador del sistema')

        target.is_superuser = is_superuser
        target.is_staff = is_superuser

        target.save()

        return {
            'message': f'Rol actualizado a {"admin" if is_superuser else "terapeuta"}',
            'username': target.username,
            'is_superuser': is_superuser,
        }
