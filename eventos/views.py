from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import EventoSerializer, TipoEventoSerializer
from .services import EventoService, TipoEventoService


_evento_service = EventoService()
_tipoevento_service = TipoEventoService()


@extend_schema_view(
    list=extend_schema(tags=['eventos']),
    retrieve=extend_schema(tags=['eventos']),
    create=extend_schema(tags=['eventos']),
    update=extend_schema(tags=['eventos']),
    partial_update=extend_schema(tags=['eventos']),
    destroy=extend_schema(tags=['eventos']),
)
class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _evento_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['eventos']),
    retrieve=extend_schema(tags=['eventos']),
    create=extend_schema(tags=['eventos']),
    update=extend_schema(tags=['eventos']),
    partial_update=extend_schema(tags=['eventos']),
    destroy=extend_schema(tags=['eventos']),
)
class TipoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoEventoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _tipoevento_service.listar()
