from rest_framework import serializers
from .models import Persona, PersonaEp, Direccion, Localidad, Municipio, Provincia, Tipoparentesco


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion', 'borrado', 'espaciente', 'sexo', 'fechanacimiento')
        extra_kwargs = {'iddireccion': {'allow_null': True, 'required': False}}


class PersonaEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaEp
        fields = '__all__'
        extra_kwargs = {
            'sexo': {'required': True, 'allow_null': False},
            'fechanacimiento': {'required': True, 'allow_null': False},
        }


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'idlocalidad')
        extra_kwargs = {'idlocalidad': {'allow_null': True, 'required': False},
                        'departamento': {'allow_null': True, 'required': False},
                        'piso': {'allow_null': True, 'required': False}}


class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idlocalidad', 'nombre', 'codigopostal', 'idmunicipio')
        extra_kwargs = {'idmunicipio': {'allow_null': True, 'required': False}}


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('idprovincia', 'nombre')


class MunicipioSerializer(serializers.ModelSerializer):
    provincia = serializers.CharField(source='idprovincia.nombre', read_only=True, allow_null=True)

    class Meta:
        model = Municipio
        fields = ('idmunicipio', 'nombre', 'provincia', 'idprovincia')
        extra_kwargs = {'idprovincia': {'allow_null': True, 'required': False}}

    def validate(self, attrs):
        if self.initial_data.get('provincia') is not None:
            raise serializers.ValidationError({
                'provincia': "El campo 'provincia' es de solo lectura en el contrato normalizado; use 'idprovincia' con el ID del catálogo /api/v1/provincias."
            })
        return attrs


class TipoparentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoparentesco
        fields = ('idpersona', 'idpersonaep', 'nombre')
