from rest_framework import serializers
from core.fields import StrictBooleanField
from .models import Obrasocial, Cobertura


class ObraSocialSerializer(serializers.ModelSerializer):
    esestatal = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Obrasocial
        fields = ('idobrasocial', 'nombre', 'esestatal')


class CoberturaSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Cobertura
        fields = ('idcobertura', 'idpersonaep', 'idobrasocial', 'borrado')


class CoberturaEpSerializer(CoberturaSerializer):
    idobrasocial = ObraSocialSerializer(many=False, read_only=True)

    class Meta(CoberturaSerializer.Meta):
        pass
