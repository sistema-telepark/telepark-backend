from rest_framework import serializers
from core.fields import StrictBooleanField
from .models import Evento, Tipoevento


class TipoEventoSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Tipoevento
        fields = ('idtipoevento', 'nombre', 'desactivataller', 'borrado')


class EventoSerializer(serializers.ModelSerializer):
    tipo_evento = TipoEventoSerializer(many=False, read_only=True, source='idtipoevento')
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Evento
        fields = ('idevento', 'fechadesde', 'fechahasta', 'motivo', 'idpersonaep', 'idtipoevento', 'tipo_evento', 'borrado')
