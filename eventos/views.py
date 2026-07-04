from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import EventoSerializer, TipoEventoSerializer
from .services import EventoService, TipoEventoService


_evento_service = EventoService()
_tipoevento_service = TipoEventoService()


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = _evento_service.listar()
    permission_classes = [IsAuthenticated]


class TipoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoEventoSerializer
    queryset = _tipoevento_service.listar()
    permission_classes = [IsAuthenticated]
