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


class EnfermedadViewSet(viewsets.ModelViewSet):
    serializer_class = EnfermedadSerializer
    queryset = _enfermedad_service.listar()
    permission_classes = [IsAuthenticated]


class MedicamentoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    queryset = _medicamento_service.listar()
    permission_classes = [IsAuthenticated]


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
