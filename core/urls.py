from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from core.views import health_check, api_root
from salud.views import DiagnosticoPorPersonaEpView, EvolucionPorPersonaEpView, IndicacionPorPersonaEpView
from obra_social.views import OsPorPersonaEpView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='api-v1-root', permanent=False), name='root-redirect'),

    path('api/v1/', api_root, name='api-v1-root'),

    path('', include('autenticacion.urls')),

    path('api/v1/health', health_check, name='health-check'),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('', include('personas.urls')),
    path('', include('salud.urls')),
    path('', include('eventos.urls')),
    path('', include('obra_social.urls')),
    path('', include('talleres.urls')),

    path('api/v1/personas-ep/<int:personaep_pk>/diagnosticos', DiagnosticoPorPersonaEpView.as_view(), name='personas-ep-diagnosticos'),
    path('api/v1/personas-ep/<int:personaep_pk>/evoluciones', EvolucionPorPersonaEpView.as_view(), name='personas-ep-evoluciones'),
    path('api/v1/personas-ep/<int:personaep_pk>/indicaciones', IndicacionPorPersonaEpView.as_view(), name='personas-ep-indicaciones'),
    path('api/v1/personas-ep/<int:personaep_pk>/coberturas', OsPorPersonaEpView.as_view(), name='personas-ep-coberturas'),
]
