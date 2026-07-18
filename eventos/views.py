from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import EventoSerializer, TipoEventoSerializer
from .models import Evento, Tipoevento


@auto_tag_schema_view
class EventoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'eventos'
    manager = Evento.objects
    serializer_class = EventoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class TipoEventoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'eventos'
    manager = Tipoevento.objects
    serializer_class = TipoEventoSerializer
    permission_classes = [IsAuthenticated]
