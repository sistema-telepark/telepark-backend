from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import EventoSerializer, TipoEventoSerializer
from .services import EventoService, TipoEventoService


_evento_service = EventoService()
_tipoevento_service = TipoEventoService()


@auto_tag_schema_view
class EventoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'eventos'
    service = _evento_service
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class TipoEventoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'eventos'
    service = _tipoevento_service
    serializer_class = TipoEventoSerializer
    permission_classes = [IsAuthenticated]
