from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import ModelPKMixin, NoPaginationMixin, PersonaEPSubresourceMixin, auto_tag_schema_view
from core.permission import AdminOrReadOnly
from core.schema import error_response

from .models import (
    Diagnostico,
    Enfermedad,
    Evolucion,
    IndicacionMedicamento,
    Medicamento,
)
from .serializers import (
    DiagnosticoEPSerializer,
    DiagnosticoSerializer,
    EnfermedadSerializer,
    EvolucionSerializer,
    IndicacionEPSerializer,
    IndicacionSerializer,
    MedicamentoSerializer,
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
    permission_classes = [AdminOrReadOnly]


@auto_tag_schema_view
class MedicamentoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = Medicamento.objects
    serializer_class = MedicamentoSerializer
    permission_classes = [AdminOrReadOnly]


@auto_tag_schema_view
class IndicacionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'salud'
    manager = IndicacionMedicamento.objects
    serializer_class = IndicacionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=['salud'],
    responses={404: error_response(404, 'PersonaEP no encontrada')},
)
class DiagnosticoPorPersonaEPView(PersonaEPSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DiagnosticoEPSerializer
    queryset = Diagnostico.objects.none()

    def get(self, request, persona_ep_pk):
        self.validar_persona_ep(persona_ep_pk)
        diagnosticos = Diagnostico.objects.filtrar_por_persona_ep(persona_ep_pk, select_related_fields=['enfermedad'])
        serializer = self.get_serializer(diagnosticos, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['salud'],
    responses={404: error_response(404, 'PersonaEP no encontrada')},
)
class EvolucionPorPersonaEPView(PersonaEPSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EvolucionSerializer
    queryset = Evolucion.objects.none()

    def get(self, request, persona_ep_pk):
        self.validar_persona_ep(persona_ep_pk)
        evoluciones = Evolucion.objects.filtrar_por_persona_ep(persona_ep_pk)
        serializer = self.get_serializer(evoluciones, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['salud'],
    responses={404: error_response(404, 'PersonaEP no encontrada')},
)
class IndicacionPorPersonaEPView(PersonaEPSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IndicacionEPSerializer
    queryset = IndicacionMedicamento.objects.none()

    def get(self, request, persona_ep_pk):
        self.validar_persona_ep(persona_ep_pk)
        indicaciones = IndicacionMedicamento.objects.filtrar_por_persona_ep(
            persona_ep_pk, select_related_fields=['medicamento']
        )
        serializer = self.get_serializer(indicaciones, many=True)
        return Response(serializer.data)
