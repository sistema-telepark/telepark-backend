from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_obrasocialP(self, request, pk):
        obrasociales = _os_service.filtrar_por_persona(pk, select_related_fields=['idobrasocial'])
        serializer = OSEpSerializer(obrasociales, many=True)
        return Response(serializer.data)
