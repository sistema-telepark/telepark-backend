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


class ObraSocialViewSet(viewsets.ModelViewSet):
    serializer_class = ObraSocialSerializer
    queryset = _obrasocial_service.listar()
    permission_classes = [IsAuthenticated]


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
