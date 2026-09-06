from rest_framework.routers import SimpleRouter
from .views import (
    PersonaViewSet, PersonaEPViewSet,
    DireccionViewSet, TipoParentescoViewSet,
    LocalidadViewSet, DepartamentoViewSet, ProvinciaViewSet,
)

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/personas', PersonaViewSet, basename='personas')
router.register(r'api/v1/personas-ep', PersonaEPViewSet, basename='personas-ep')
router.register(r'api/v1/direcciones', DireccionViewSet, basename='direcciones')
router.register(r'api/v1/tipos-parentesco', TipoParentescoViewSet, basename='tipos-parentesco')
router.register(r'api/v1/localidades', LocalidadViewSet, basename='localidades')
router.register(r'api/v1/departamentos', DepartamentoViewSet, basename='departamentos')
router.register(r'api/v1/provincias', ProvinciaViewSet, basename='provincias')

urlpatterns = router.urls
