from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

from core.mixins import ModelPKMixin, NoPaginationMixin, PersonaEpSubresourceMixin, auto_tag_schema_view
from core.permission import AdminOrReadOnly
from core.schema import error_response

from .serializers import (
    ObraSocialSerializer, CoberturaEpSerializer, CoberturaSerializer,
)
from .models import Obrasocial, Cobertura


@auto_tag_schema_view
class ObraSocialViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    manager = Obrasocial.objects
    serializer_class = ObraSocialSerializer
    permission_classes = [AdminOrReadOnly]


@auto_tag_schema_view
class CoberturaViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    manager = Cobertura.objects
    serializer_class = CoberturaSerializer
    permission_classes = [AdminOrReadOnly]


@extend_schema(
    tags=['obra_social'],
    responses={404: error_response(404, "PersonaEp no encontrada")},
)
class CoberturaPorPersonaEpView(PersonaEpSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoberturaEpSerializer
    queryset = Cobertura.objects.none()

    def get(self, request, personaep_pk):
        self.validar_personaep(personaep_pk)
        obrasociales = Cobertura.objects.filtrar_por_persona_ep(personaep_pk, select_related_fields=['idobrasocial'])
        serializer = self.get_serializer(obrasociales, many=True)
        return Response(serializer.data)
