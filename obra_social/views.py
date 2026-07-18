from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import (
    ObraSocialSerializer, OSEpSerializer, OSSerializer,
)
from .models import Obrasocial, Os


@auto_tag_schema_view
class ObraSocialViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    manager = Obrasocial.objects
    serializer_class = ObraSocialSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class OSViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    manager = Os.objects
    serializer_class = OSSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['obra_social'])
class OsPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OSEpSerializer
    queryset = Os.objects.none()

    def get(self, request, personaep_pk):
        obrasociales = Os.objects.filtrar_por_persona(personaep_pk, select_related_fields=['idobrasocial'])
        serializer = self.get_serializer(obrasociales, many=True)
        return Response(serializer.data)
