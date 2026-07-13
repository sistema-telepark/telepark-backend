from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.views import health_check, api_root
from salud.views import DiagnosticoPorPersonaEpView, EvolucionPorPersonaEpView, IndicacionPorPersonaEpView
from obra_social.views import OsPorPersonaEpView

urlpatterns = [
    # Redirect / → /api/
    path('', RedirectView.as_view(pattern_name='global-api-root', permanent=False), name='root-redirect'),

    # API Root global
    path('api/', api_root, name='global-api-root'),

    # Autenticación y gestión de usuarios — delegado al módulo autenticacion
    path('', include('autenticacion.urls')),
    path('api/health', health_check, name='health_check'),

    # Documentación OpenAPI / Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Módulos de dominio
    path('', include('personas.urls')),
    path('', include('salud.urls')),
    path('', include('eventos.urls')),
    path('', include('obra_social.urls')),
    path('', include('talleres.urls')),

    # Rutas personaEp → sub-recursos (reemplazan @action mal diseñados)
    path('api/personaEp/<int:personaep_pk>/diagnostico', DiagnosticoPorPersonaEpView.as_view(), name='personaEp-diagnostico'),
    path('api/personaEp/<int:personaep_pk>/evolucion', EvolucionPorPersonaEpView.as_view(), name='personaEp-evolucion'),
    path('api/personaEp/<int:personaep_pk>/indicacion', IndicacionPorPersonaEpView.as_view(), name='personaEp-indicacion'),
    path('api/personaEp/<int:personaep_pk>/os', OsPorPersonaEpView.as_view(), name='personaEp-os'),
]
