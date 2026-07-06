from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

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
class ObraSocialViewSet(viewsets.ModelViewSet):
    serializer_class = ObraSocialSerializer
    queryset = _obrasocial_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['obra_social']),
    retrieve=extend_schema(tags=['obra_social']),
    create=extend_schema(tags=['obra_social']),
    update=extend_schema(tags=['obra_social']),
    partial_update=extend_schema(tags=['obra_social']),
    destroy=extend_schema(tags=['obra_social']),
    list_obrasocialP=extend_schema(tags=['obra_social']),
)
class OSViewSet(viewsets.ModelViewSet):
    serializer_class = OSSerializer
    queryset = _os_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_obrasocialP(self, request, pk):
        obrasociales = _os_service.filtrar_por_persona(pk)
        serializer = OSEpSerializer(obrasociales, many=True)
        return Response(serializer.data)
