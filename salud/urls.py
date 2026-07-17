from rest_framework.routers import SimpleRouter
from .views import (
    DiagnosticoViewSet, EvolucionViewSet, EnfermedadViewSet,
    MedicamentoViewSet, IndicacionViewSet,
)

router = SimpleRouter(trailing_slash=False)

router.register(r'api/v1/diagnosticos', DiagnosticoViewSet, basename='diagnosticos')
router.register(r'api/v1/evoluciones', EvolucionViewSet, basename='evoluciones')
router.register(r'api/v1/enfermedades', EnfermedadViewSet, basename='enfermedades')
router.register(r'api/v1/medicamentos', MedicamentoViewSet, basename='medicamentos')
router.register(r'api/v1/indicaciones', IndicacionViewSet, basename='indicaciones')

urlpatterns = router.urls
