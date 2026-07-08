from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.mixins import ModelPKMixin

from .serializers import (
    ObraSocialSerializer, OSEpSerializer, OSSerializer,
)
from .services import ObraSocialService, OsService


_obrasocial_service = ObraSocialService()
_os_service = OsService()


@extend_schema_view(
    list=extend_schema(tags=['obra_social']),
    retrieve=extend_schema(tags=['obra_social']),
    create=extend_schema(tags=['obra_social']),
    update=extend_schema(tags=['obra_social']),
    partial_update=extend_schema(tags=['obra_social']),
    destroy=extend_schema(tags=['obra_social']),
)
class ObraSocialViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _obrasocial_service
    serializer_class = ObraSocialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _obrasocial_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['obra_social']),
    retrieve=extend_schema(tags=['obra_social']),
    create=extend_schema(tags=['obra_social']),
    update=extend_schema(tags=['obra_social']),
    partial_update=extend_schema(tags=['obra_social']),
    destroy=extend_schema(tags=['obra_social']),
    list_obrasocialP=extend_schema(tags=['obra_social']),
)
class OSViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _os_service
    serializer_class = OSSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _os_service.listar()

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_obrasocialP(self, request, pk):
        obrasociales = _os_service.filtrar_por_persona(pk)
        serializer = OSEpSerializer(obrasociales, many=True)
        return Response(serializer.data)
