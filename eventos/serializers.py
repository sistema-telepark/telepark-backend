from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import Evento, TipoEvento


class TipoEventoSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)
    desactiva_taller = StrictBooleanField(required=False, default=False)

    class Meta:
        model = TipoEvento
        fields = ('id_tipo_evento', 'nombre', 'desactiva_taller', 'borrado')


class EventoSerializer(serializers.ModelSerializer):
    tipo_evento_detalle = TipoEventoSerializer(many=False, read_only=True, source='tipo_evento')
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Evento
        fields = (
            'id_evento',
            'fecha_desde',
            'fecha_hasta',
            'motivo',
            'persona_ep',
            'tipo_evento',
            'tipo_evento_detalle',
            'borrado',
        )
