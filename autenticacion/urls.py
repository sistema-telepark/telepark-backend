from django.urls import path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenRefreshView

from autenticacion import views

refresh_view = extend_schema_view(
    post=extend_schema(tags=['autenticacion']),
)(TokenRefreshView).as_view()

urlpatterns = [
    path('api/v1/auth/login', views.auth_view, name='auth-login'),
    path('api/v1/auth/refresh', refresh_view, name='auth-refresh'),
    path('api/v1/usuarios', views.usuarios_list, name='usuarios-list'),
    path('api/v1/usuarios/<int:id_usuario>', views.usuarios_detail, name='usuarios-detail'),
]
