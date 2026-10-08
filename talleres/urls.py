from rest_framework.routers import SimpleRouter
from .views import (
    TallerViewSet, EncuentroViewSet, ActividadViewSet,
    EncuentroActividadViewSet, AsistenciaTallerViewSet,
    EncuentroFactorGlobalViewSet,
    FactorGlobalViewSet, UnidadObservacionViewSet,
    VariableUOViewSet, ValorVariableUOViewSet,
)

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/talleres', TallerViewSet, basename='talleres')
router.register(r'api/v1/encuentros', EncuentroViewSet, basename='encuentros')
router.register(r'api/v1/actividades', ActividadViewSet, basename='actividades')
router.register(r'api/v1/encuentros-actividades', EncuentroActividadViewSet, basename='encuentros-actividades')
router.register(r'api/v1/asistencias-taller', AsistenciaTallerViewSet, basename='asistencias-taller')
router.register(r'api/v1/encuentros-factores-globales', EncuentroFactorGlobalViewSet, basename='encuentros-factores-globales')
router.register(r'api/v1/factores-globales', FactorGlobalViewSet, basename='factores-globales')
router.register(r'api/v1/unidades-observacion', UnidadObservacionViewSet, basename='unidades-observacion')
router.register(r'api/v1/variables-uo', VariableUOViewSet, basename='variables-uo')
router.register(r'api/v1/valores-variable-uo', ValorVariableUOViewSet, basename='valores-variable-uo')

urlpatterns = router.urls
