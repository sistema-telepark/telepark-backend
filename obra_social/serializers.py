from rest_framework import serializers
from .models import Obrasocial, Os


class ObraSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obrasocial
        fields = ('idobrasocial', 'nombre', 'esestatal')


class OSEpSerializer(serializers.ModelSerializer):
    idobrasocial = ObraSocialSerializer(many=False, read_only=True)

    class Meta:
        model = Os
        fields = ('idos', 'idpersonaep', 'idobrasocial', 'borrado')


class OSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Os
        fields = ('idos', 'idpersonaep', 'idobrasocial', 'borrado')
