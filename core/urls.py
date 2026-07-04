from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from core import authentication
from core.views import health_check

urlpatterns = [
    # Autenticación
    path('api/login', authentication.auth_view),
    path('api/create_user', authentication.create_user),
    path('api/refresh_token', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users', authentication.get_users),
    path('api/update_user', authentication.update_user),
    path('api/health', health_check, name='health_check'),

    # Módulos de dominio
    path('', include('personas.urls')),
    path('', include('salud.urls')),
    path('', include('eventos.urls')),
    path('', include('obra_social.urls')),
    path('', include('talleres.urls')),
]
