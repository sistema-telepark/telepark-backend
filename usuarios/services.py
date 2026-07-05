from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UsuarioService:
    """Lógica de negocio para autenticación y gestión de usuarios."""

    @staticmethod
    def autenticar(data):
        """
        Valida credenciales y retorna JWT.
        Lanza AuthenticationFailed (401) si las credenciales son inválidas
        o el usuario está deshabilitado.
        """
        username = data.get('username')
        password = data.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Credenciales inválidas')

        if not check_password(password, user.password):
            raise AuthenticationFailed('Credenciales inválidas')

        if not user.is_active:
            raise AuthenticationFailed('El usuario está deshabilitado')

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
        """
        Crea un nuevo usuario Django.
        Lanza ValidationError (400) si el username ya existe.
        """
        username = data.get('user')

        if User.objects.filter(username=username).exists():
            raise ValidationError('El usuario ya existe')

        User.objects.create_user(
            username=username,
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            password=data.get('password'),
            is_superuser=data.get('is_superuser'),
            is_staff=data.get('is_staff'),
            is_active=data.get('is_active'),
        )

        return {'message': 'Usuario creado correctamente'}

    @staticmethod
    def actualizar(data):
        """
        Actualización parcial de un usuario existente.
        Lanza ValidationError (400) si el usuario no existe.
        """
        username = data.get('user')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError('Usuario no encontrado')

        if 'password' in data:
            user.set_password(data['password'])
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'is_active' in data:
            user.is_active = data['is_active']
        if 'is_superuser' in data:
            user.is_superuser = data['is_superuser']
        if 'is_staff' in data:
            user.is_staff = data['is_staff']

        user.save()

        return {'message': 'Usuario actualizado correctamente'}

    @staticmethod
    def listar():
        """Retorna queryset de todos los usuarios."""
        return User.objects.all()
