from rest_framework import serializers
from .models import Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion', 'borrado', 'espaciente')


class PersonaEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaEp
        fields = ('activataller',
                  'escolaridadcompleta',
                  'fechainicio',
                  'fechanacimiento',
                  'maximaescolaridadalcanzada',
                  'sexo',
                  'tieneacompanante',
                  'tienecuidador',
                  'vivesolo',
                  'ocupacionprevia',
                  'ocupacionactual',
                  'idpersona',
                  'idreferente')


class PersonaPSerializer(serializers.ModelSerializer):
    idpersona = PersonaSerializer(many=False, read_only=True)

    class Meta:
        model = PersonaEp
        fields = ('sexo', 'idpersona')


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'idlocalidad')


class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idlocalidad', 'nombre', 'codigopostal', 'idmunicipio')


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('idmunicipio', 'nombre', 'provincia')


class TipoparentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoparentesco
        fields = ('idpersona', 'idpersonaep', 'nombre')
