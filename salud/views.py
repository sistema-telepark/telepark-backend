from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

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



@auto_tag_schema_view
class EvolucionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    service = _evolucion_service
    serializer_class = EvolucionSerializer
    permission_classes = [IsAuthenticated]



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


@extend_schema(tags=['salud'])
class DiagnosticoPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiagnosticoEpSerializer
    queryset = _diagnostico_service.model.objects.none()

    def get(self, request, personaep_pk):
        diagnosticos = _diagnostico_service.filtrar_por_persona(personaep_pk, select_related_fields=['idenfermedad'])
        serializer = self.get_serializer(diagnosticos, many=True)
        return Response(serializer.data)


@extend_schema(tags=['salud'])
class EvolucionPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvolucionSerializer
    queryset = _evolucion_service.model.objects.none()

    def get(self, request, personaep_pk):
        evoluciones = _evolucion_service.filtrar_por_persona(personaep_pk)
        serializer = self.get_serializer(evoluciones, many=True)
        return Response(serializer.data)


@extend_schema(tags=['salud'])
class IndicacionPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicacionEpSerializer
    queryset = _indicacion_service.model.objects.none()

    def get(self, request, personaep_pk):
        indicaciones = _indicacion_service.filtrar_por_persona(personaep_pk, select_related_fields=['idmedicamento'])
        serializer = self.get_serializer(indicaciones, many=True)
        return Response(serializer.data)


