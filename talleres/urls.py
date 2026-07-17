from rest_framework.routers import SimpleRouter
from .views import (
    TallerViewSet, ClaseTallerViewSet, ActividadViewSet,
    ActividadRealizadaViewSet, AsistenciaTallerViewSet,
    ComportamientoViewSet, FactorClaseViewSet,
    FactorGlobalViewSet, UnidadObservacionViewSet,
    VariableUOViewSet, ValorVariableUOViewSet,
)

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/talleres', TallerViewSet, basename='talleres')
router.register(r'api/v1/clases-taller', ClaseTallerViewSet, basename='clases-taller')
router.register(r'api/v1/actividades', ActividadViewSet, basename='actividades')
router.register(r'api/v1/actividades-realizadas', ActividadRealizadaViewSet, basename='actividades-realizadas')
router.register(r'api/v1/asistencias-taller', AsistenciaTallerViewSet, basename='asistencias-taller')
router.register(r'api/v1/comportamientos', ComportamientoViewSet, basename='comportamientos')
router.register(r'api/v1/factores-clase', FactorClaseViewSet, basename='factores-clase')
router.register(r'api/v1/factores-globales', FactorGlobalViewSet, basename='factores-globales')
router.register(r'api/v1/unidades-observacion', UnidadObservacionViewSet, basename='unidades-observacion')
router.register(r'api/v1/variables-uo', VariableUOViewSet, basename='variables-uo')
router.register(r'api/v1/valores-variable-uo', ValorVariableUOViewSet, basename='valores-variable-uo')

urlpatterns = router.urls
