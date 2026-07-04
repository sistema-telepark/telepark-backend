from rest_framework import serializers
from .models import Evento, Tipoevento


class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoevento
        fields = ('idtipoevento', 'nombre', 'desactivataller', 'borrado')


class EventoSerializer(serializers.ModelSerializer):
    tipoEvento = TipoEventoSerializer(many=False, read_only=True)

    class Meta:
        model = Evento
        fields = ('idevento', 'fechadesde', 'fechahasta', 'motivo', 'idpersonaep', 'idtipoevento', 'tipoEvento', 'borrado')
