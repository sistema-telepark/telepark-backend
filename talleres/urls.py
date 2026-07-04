from rest_framework.routers import DefaultRouter
from .views import (
    TallerViewSet, ClaseTallerViewSet, ActividadViewSet,
    ActividadRealizadaViewSet, AsistenciaTallerViewSet,
    ComportamientoViewSet, FactorClaseViewSet,
    FactorGlobalViewSet, UnidadObservacionViewSet,
    VariableUOViewSet, ValorVariableUOViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r'api/taller', TallerViewSet, basename='taller')
router.register(r'api/clasetaller', ClaseTallerViewSet, basename='clasetaller')
router.register(r'api/actividad', ActividadViewSet, basename='actividad')
router.register(r'api/actividadrealizada', ActividadRealizadaViewSet, basename='actividadrealizada')
router.register(r'api/asistenciataller', AsistenciaTallerViewSet, basename='asistenciataller')
router.register(r'api/comportamiento', ComportamientoViewSet, basename='comportamiento')
router.register(r'api/factorclase', FactorClaseViewSet, basename='factorclase')
router.register(r'api/factorglobal', FactorGlobalViewSet, basename='factorglobal')
router.register(r'api/unidadobservacion', UnidadObservacionViewSet, basename='unidadobservacion')
router.register(r'api/variableuo', VariableUOViewSet, basename='variableuo')
router.register(r'api/valorvariableuo', ValorVariableUOViewSet, basename='valorvariableuo')

urlpatterns = router.urls
