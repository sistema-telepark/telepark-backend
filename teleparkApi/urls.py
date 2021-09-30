from teleparkApi.serializers import EventoSerializer
from rest_framework.routers import DefaultRouter
from django.conf.urls import url 
from . import authentication
from .api import DiagnosticoViewSet, DireccionViewSet, EnfermedadViewSet, EventoViewSet, LocalidadViewSet, MunicipioViewSet, PersonaEPViewSet, PersonaViewSet, TipoEventoViewSet, TipoParentescoViewSet

app_name = 'teleparkApi'

router = DefaultRouter(trailing_slash=False)

router.register(r'api/persona', PersonaViewSet, basename = 'persona')
router.register(r'api/personaEp', PersonaEPViewSet, basename = 'personaEp')
router.register(r'api/direccion', DireccionViewSet, basename = 'direccion')
router.register(r'api/tipoparentesco', TipoParentescoViewSet, basename = 'tipoparentesco')
router.register(r'api/localidad', LocalidadViewSet, basename = 'localidad')
router.register(r'api/municipio', MunicipioViewSet, basename = 'municipio')
router.register(r'api/evento', EventoViewSet, basename = 'evento')
router.register(r'api/tipoevento', TipoEventoViewSet, basename = 'tipoevento')
router.register(r'api/enfermedad', EnfermedadViewSet, basename = 'enfermedad')
router.register(r'api/diagnostico', DiagnosticoViewSet, basename = 'diagnostico')

urlpatterns = [ 
    url(r'^api/auth$', authentication.auth_view)
]

urlpatterns += router.urls