from django.db import transaction
from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import Departamento, Direccion, Localidad, Persona, PersonaEP, Provincia, TipoParentesco


class PersonaSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Persona
        fields = ('id_persona', 'nombre', 'apellido', 'telefono', 'direccion', 'borrado', 'sexo', 'fecha_nacimiento')
        extra_kwargs = {'direccion': {'allow_null': True, 'required': False}}


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('id_direccion', 'calle', 'departamento', 'numero', 'piso', 'localidad')
        extra_kwargs = {
            'localidad': {'allow_null': True, 'required': False},
            'departamento': {'allow_null': True, 'required': False},
            'piso': {'allow_null': True, 'required': False},
        }


class ReferenteSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Persona
        fields = ('nombre', 'apellido', 'telefono', 'sexo', 'fecha_nacimiento', 'direccion')
        extra_kwargs = {
            'sexo': {'required': False, 'allow_null': True},
            'fecha_nacimiento': {'required': False, 'allow_null': True},
        }


class PersonaEPSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer(write_only=True, required=False, allow_null=True)
    referente = ReferenteSerializer(write_only=True)
    direccion_id = serializers.IntegerField(read_only=True)
    referente_id = serializers.IntegerField(read_only=True)
    activa_taller = StrictBooleanField(required=False, default=False)
    escolaridad_completa = StrictBooleanField(required=False, default=False)
    tiene_acompanante = StrictBooleanField(required=False, default=False)
    tiene_cuidador = StrictBooleanField(required=False, default=False)
    vive_solo = StrictBooleanField(required=False, default=False)

    class Meta:
        model = PersonaEP
        fields = (
            'id_persona',
            'nombre',
            'apellido',
            'telefono',
            'direccion_id',
            'borrado',
            'sexo',
            'fecha_nacimiento',
            'activa_taller',
            'escolaridad_completa',
            'fecha_inicio',
            'maxima_escolaridad_alcanzada',
            'tiene_acompanante',
            'tiene_cuidador',
            'vive_solo',
            'ocupacion_previa',
            'ocupacion_actual',
            'referente_id',
            'direccion',
            'referente',
        )
        extra_kwargs = {
            'borrado': {'read_only': True},
            'sexo': {'required': False, 'allow_null': True},
            'fecha_nacimiento': {'required': False, 'allow_null': True},
        }

    def create(self, validated_data):
        with transaction.atomic():
            referente_data = validated_data.pop('referente')
            direccion_data = validated_data.pop('direccion', None)

            referente_direccion_data = referente_data.pop('direccion', None)
            referente_direccion = (
                Direccion.objects.create(**referente_direccion_data) if referente_direccion_data else None
            )
            referente = Persona.objects.create(
                **referente_data,
                borrado=False,
                direccion=referente_direccion,
            )

            direccion = Direccion.objects.create(**direccion_data) if direccion_data else None

            validated_data['direccion'] = direccion
            validated_data['referente'] = referente
            validated_data['borrado'] = False
            return super().create(validated_data)


class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('id_localidad', 'nombre', 'codigo_postal', 'departamento')
        extra_kwargs = {'departamento': {'allow_null': True, 'required': False}}


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = ('id_provincia', 'nombre')


class DepartamentoSerializer(serializers.ModelSerializer):
    provincia_nombre = serializers.CharField(source='provincia.nombre', read_only=True, allow_null=True)

    class Meta:
        model = Departamento
        fields = ('id_departamento', 'nombre', 'provincia_nombre', 'provincia')
        extra_kwargs = {'provincia': {'allow_null': True, 'required': False}}

    def validate(self, attrs):
        if self.initial_data.get('provincia_nombre') is not None:
            raise serializers.ValidationError(
                {
                    'provincia_nombre': "El campo 'provincia_nombre' es de solo lectura en el contrato normalizado; use 'provincia' con el ID del catálogo /api/v1/provincias."
                }
            )
        return attrs


class TipoParentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoParentesco
        fields = ('persona', 'persona_ep', 'nombre')
