from rest_framework.routers import DefaultRouter
from .views import (
    PersonaViewSet, PersonaEPViewSet,
    DireccionViewSet, TipoParentescoViewSet,
    LocalidadViewSet, MunicipioViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r'api/persona', PersonaViewSet, basename='persona')
router.register(r'api/personaEp', PersonaEPViewSet, basename='personaEp')
router.register(r'api/direccion', DireccionViewSet, basename='direccion')
router.register(r'api/tipoparentesco', TipoParentescoViewSet, basename='tipoparentesco')
router.register(r'api/localidad', LocalidadViewSet, basename='localidad')
router.register(r'api/municipio', MunicipioViewSet, basename='municipio')

urlpatterns = router.urls
