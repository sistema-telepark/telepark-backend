from rest_framework import serializers
from .models import Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion', 'borrado', 'espaciente')
        extra_kwargs = {'iddireccion': {'allow_null': True, 'required': False}}


class PersonaEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaEp
        fields = '__all__'


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'idlocalidad')
        extra_kwargs = {'idlocalidad': {'allow_null': True, 'required': False}}


class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idlocalidad', 'nombre', 'codigopostal', 'idmunicipio')
        extra_kwargs = {'idmunicipio': {'allow_null': True, 'required': False}}


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('idmunicipio', 'nombre', 'provincia')


class TipoparentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoparentesco
        fields = ('idpersona', 'idpersonaep', 'nombre')
