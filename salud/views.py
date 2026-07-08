from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import ModelPKMixin

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


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
    list_diagnosticoP=extend_schema(tags=['salud']),
)
class DiagnosticoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _diagnostico_service
    serializer_class = DiagnosticoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _diagnostico_service.listar()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_diagnosticoP(self, request, pk):
        diagnosticos = _diagnostico_service.filtrar_por_persona(pk)
        serializer = DiagnosticoEpSerializer(diagnosticos, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
    list_evolucionP=extend_schema(tags=['salud']),
)
class EvolucionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _evolucion_service
    serializer_class = EvolucionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _evolucion_service.listar()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_evolucionP(self, request, pk):
        evoluciones = _evolucion_service.filtrar_por_persona(pk)
        serializer = EvolucionSerializer(evoluciones, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
)
class EnfermedadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _enfermedad_service
    serializer_class = EnfermedadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _enfermedad_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
)
class MedicamentoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _medicamento_service
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _medicamento_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
    list_indicacionP=extend_schema(tags=['salud']),
)
class IndicacionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _indicacion_service
    serializer_class = IndicacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _indicacion_service.listar()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_indicacionP(self, request, pk):
        indicaciones = _indicacion_service.filtrar_por_persona(pk)
        serializer = IndicacionEpSerializer(indicaciones, many=True)
        return Response(serializer.data)
