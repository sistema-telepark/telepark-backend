from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import (
    EvolucionSerializer, DiagnosticoEpSerializer, DiagnosticoSerializer,
    MedicamentoSerializer, IndicacionEpSerializer,
    IndicacionSerializer, EnfermedadSerializer,
)
from .services import (
    DiagnosticoService, EvolucionService,
    IndicacionService, MedicamentoService,
    EnfermedadService,
)


_diagnostico_service = DiagnosticoService()
_evolucion_service = EvolucionService()
_enfermedad_service = EnfermedadService()
_medicamento_service = MedicamentoService()
_indicacion_service = IndicacionService()


@auto_tag_schema_view
class DiagnosticoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _diagnostico_service
    serializer_class = DiagnosticoSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_diagnosticoP(self, request, pk):
        diagnosticos = _diagnostico_service.filtrar_por_persona(pk, select_related_fields=['idenfermedad'])
        serializer = DiagnosticoEpSerializer(diagnosticos, many=True)
        return Response(serializer.data)


@auto_tag_schema_view
class EvolucionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _evolucion_service
    serializer_class = EvolucionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_evolucionP(self, request, pk):
        evoluciones = _evolucion_service.filtrar_por_persona(pk)
        serializer = EvolucionSerializer(evoluciones, many=True)
        return Response(serializer.data)


@auto_tag_schema_view
class EnfermedadViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _enfermedad_service
    serializer_class = EnfermedadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class MedicamentoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _medicamento_service
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class IndicacionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _indicacion_service
    serializer_class = IndicacionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_indicacionP(self, request, pk):
        indicaciones = _indicacion_service.filtrar_por_persona(pk, select_related_fields=['idmedicamento'])
        serializer = IndicacionEpSerializer(indicaciones, many=True)
        return Response(serializer.data)
