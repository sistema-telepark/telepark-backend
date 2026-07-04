from rest_framework.routers import DefaultRouter
from .views import (
    DiagnosticoViewSet, EvolucionViewSet, EnfermedadViewSet,
    MedicamentoViewSet, IndicacionViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r'api/diagnostico', DiagnosticoViewSet, basename='diagnostico')
router.register(r'api/evolucion', EvolucionViewSet, basename='evolucion')
router.register(r'api/enfermedad', EnfermedadViewSet, basename='enfermedad')
router.register(r'api/medicamento', MedicamentoViewSet, basename='medicamento')
router.register(r'api/indicacion', IndicacionViewSet, basename='indicacionmedicamento')

urlpatterns = router.urls
