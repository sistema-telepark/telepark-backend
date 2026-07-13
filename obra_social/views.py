from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from drf_spectacular.utils import extend_schema

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import (
    ObraSocialSerializer, OSEpSerializer, OSSerializer,
)
from .services import ObraSocialService, OsService


_obrasocial_service = ObraSocialService()
_os_service = OsService()


@auto_tag_schema_view
class ObraSocialViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    service = _obrasocial_service
    serializer_class = ObraSocialSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class OSViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'obra_social'
    service = _os_service
    serializer_class = OSSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['obra_social'])
class OsPorPersonaEpView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OSEpSerializer
    queryset = _os_service.model.objects.none()

    def get(self, request, personaep_pk):
        obrasociales = _os_service.filtrar_por_persona(personaep_pk, select_related_fields=['idobrasocial'])
        serializer = self.get_serializer(obrasociales, many=True)
        return Response(serializer.data)
