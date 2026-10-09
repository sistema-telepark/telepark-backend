from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import Cobertura, ObraSocial


class ObraSocialSerializer(serializers.ModelSerializer):
    es_estatal = StrictBooleanField(required=False, default=False)

    class Meta:
        model = ObraSocial
        fields = ('id_obra_social', 'nombre', 'es_estatal')


class CoberturaSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Cobertura
        fields = ('id_cobertura', 'persona_ep', 'obra_social', 'borrado')


class CoberturaEpSerializer(CoberturaSerializer):
    obra_social = ObraSocialSerializer(many=False, read_only=True)

    class Meta(CoberturaSerializer.Meta):
        pass
