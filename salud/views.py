from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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
class DiagnosticoViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosticoSerializer
    queryset = _diagnostico_service.listar()
    permission_classes = [IsAuthenticated]

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
class EvolucionViewSet(viewsets.ModelViewSet):
    serializer_class = EvolucionSerializer
    queryset = _evolucion_service.listar()
    permission_classes = [IsAuthenticated]

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
class EnfermedadViewSet(viewsets.ModelViewSet):
    serializer_class = EnfermedadSerializer
    queryset = _enfermedad_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
)
class MedicamentoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    queryset = _medicamento_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['salud']),
    retrieve=extend_schema(tags=['salud']),
    create=extend_schema(tags=['salud']),
    update=extend_schema(tags=['salud']),
    partial_update=extend_schema(tags=['salud']),
    destroy=extend_schema(tags=['salud']),
    list_indicacionP=extend_schema(tags=['salud']),
)
class IndicacionViewSet(viewsets.ModelViewSet):
    serializer_class = IndicacionSerializer
    queryset = _indicacion_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_indicacionP(self, request, pk):
        indicaciones = _indicacion_service.filtrar_por_persona(pk)
        serializer = IndicacionEpSerializer(indicaciones, many=True)
        return Response(serializer.data)
