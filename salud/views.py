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
from .models import (
    Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento,
)


@auto_tag_schema_view
class DiagnosticoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Diagnostico.objects
    serializer_class = DiagnosticoSerializer
    permission_classes = [IsAuthenticated]



@auto_tag_schema_view
class EvolucionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Evolucion.objects
    serializer_class = EvolucionSerializer
    permission_classes = [IsAuthenticated]



@auto_tag_schema_view
class EnfermedadViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Enfermedad.objects
    serializer_class = EnfermedadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class MedicamentoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Medicamento.objects
    serializer_class = MedicamentoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class IndicacionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Indicacionmedicamento.objects
    serializer_class = IndicacionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['salud'])
class DiagnosticoPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiagnosticoEpSerializer
    queryset = Diagnostico.objects.none()

    def get(self, request, personaep_pk):
        diagnosticos = Diagnostico.objects.filtrar_por_persona_ep(personaep_pk, select_related_fields=['idenfermedad'])
        serializer = self.get_serializer(diagnosticos, many=True)
        return Response(serializer.data)


@extend_schema(tags=['salud'])
class EvolucionPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvolucionSerializer
    queryset = Evolucion.objects.none()

    def get(self, request, personaep_pk):
        evoluciones = Evolucion.objects.filtrar_por_persona_ep(personaep_pk)
        serializer = self.get_serializer(evoluciones, many=True)
        return Response(serializer.data)


@extend_schema(tags=['salud'])
class IndicacionPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicacionEpSerializer
    queryset = Indicacionmedicamento.objects.none()

    def get(self, request, personaep_pk):
        indicaciones = Indicacionmedicamento.objects.filtrar_por_persona_ep(personaep_pk, select_related_fields=['idmedicamento'])
        serializer = self.get_serializer(indicaciones, many=True)
        return Response(serializer.data)


