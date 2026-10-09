from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import ModelPKMixin, NoPaginationMixin, PersonaEPSubresourceMixin, auto_tag_schema_view
from core.permission import AdminOrReadOnly
from core.schema import error_response

from .models import Cobertura, ObraSocial
from .serializers import (
    CoberturaEpSerializer,
    CoberturaSerializer,
    ObraSocialSerializer,
)


@auto_tag_schema_view
class ObraSocialViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    manager = ObraSocial.objects
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
    responses={404: error_response(404, 'PersonaEP no encontrada')},
)
class CoberturaPorPersonaEPView(PersonaEPSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CoberturaEpSerializer
    queryset = Cobertura.objects.none()

    def get(self, request, persona_ep_pk):
        self.validar_persona_ep(persona_ep_pk)
        obrasociales = Cobertura.objects.filtrar_por_persona_ep(persona_ep_pk, select_related_fields=['obra_social'])
        serializer = self.get_serializer(obrasociales, many=True)
        return Response(serializer.data)
