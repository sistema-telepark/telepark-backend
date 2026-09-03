from django.db import transaction
from rest_framework import serializers
from core.fields import StrictBooleanField
from .models import Persona, PersonaEp, Direccion, Localidad, Municipio, Provincia, Tipoparentesco


class PersonaSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion', 'borrado', 'sexo', 'fechanacimiento')
        extra_kwargs = {'iddireccion': {'allow_null': True, 'required': False}}


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


class ReferenteSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'telefono', 'sexo', 'fechanacimiento', 'direccion')
        extra_kwargs = {
            'sexo': {'required': False, 'allow_null': True},
            'fechanacimiento': {'required': False, 'allow_null': True},
        }


class PersonaEpSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(write_only=True, required=False, allow_null=True)
    referente = ReferenteSerializer(write_only=True)

    class Meta:
        model = PersonaEp
        fields = (
            'idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion',
            'borrado', 'sexo', 'fechanacimiento',
            'activataller', 'escolaridadcompleta', 'fechainicio',
            'maximaescolaridadalcanzada', 'tieneacompanante', 'tienecuidador',
            'vivesolo', 'ocupacionprevia', 'ocupacionactual', 'idreferente',
            'direccion', 'referente',
        )
        extra_kwargs = {
            'iddireccion': {'read_only': True},
            'idreferente': {'read_only': True},
            'borrado': {'read_only': True},
            'sexo': {'required': False, 'allow_null': True},
            'fechanacimiento': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            referente_data = validated_data.pop('referente')
            direccion_data = validated_data.pop('direccion', None)

            referente_direccion_data = referente_data.pop('direccion', None)
            referente_direccion = Direccion.objects.create(**referente_direccion_data) if referente_direccion_data else None
            referente = Persona.objects.create(
                **referente_data,
                borrado=False,
                iddireccion=referente_direccion,
            )

            direccion = Direccion.objects.create(**direccion_data) if direccion_data else None

            validated_data['iddireccion'] = direccion
            validated_data['idreferente'] = referente
            validated_data['borrado'] = False
            return super().create(validated_data)


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