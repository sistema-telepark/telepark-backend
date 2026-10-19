from django.db import transaction
from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import Departamento, Direccion, Localidad, Persona, PersonaEP, Provincia, TipoVinculo, Vinculo


def _actualizar_direccion(direccion, datos):
    if direccion is None:
        return Direccion.objects.create(**datos)
    for campo, valor in datos.items():
        setattr(direccion, campo, valor)
    direccion.save()
    return direccion


class PersonaSerializer(serializers.ModelSerializer):
    activo = StrictBooleanField(required=False)

    class Meta:
        model = Persona
        fields = ('id_persona', 'nombre', 'apellido', 'telefono', 'direccion', 'activo', 'sexo', 'fecha_nacimiento')
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
    activo = StrictBooleanField(required=False)
    activa_taller = StrictBooleanField(required=False)
    escolaridad_completa = StrictBooleanField(required=False)
    tiene_acompanante = StrictBooleanField(required=False)
    tiene_cuidador = StrictBooleanField(required=False)
    vive_solo = StrictBooleanField(required=False)

    class Meta:
        model = PersonaEP
        fields = (
            'id_persona',
            'nombre',
            'apellido',
            'telefono',
            'direccion_id',
            'activo',
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
                activo=True,
                direccion=referente_direccion,
            )

            direccion = Direccion.objects.create(**direccion_data) if direccion_data else None

            validated_data['direccion'] = direccion
            validated_data['referente'] = referente
            validated_data['activo'] = True
            return super().create(validated_data)

    def update(self, instance, validated_data):
        with transaction.atomic():
            referente_data = validated_data.pop('referente', None)
            direccion_data = validated_data.pop('direccion', None)

            if referente_data is not None:
                referente = instance.referente
                referente_direccion_data = referente_data.pop('direccion', None)
                if referente_direccion_data is not None:
                    referente.direccion = _actualizar_direccion(referente.direccion, referente_direccion_data)
                for campo, valor in referente_data.items():
                    setattr(referente, campo, valor)
                referente.save()

            if direccion_data is not None:
                instance.direccion = _actualizar_direccion(instance.direccion, direccion_data)

            return super().update(instance, validated_data)


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


class TipoVinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVinculo
        fields = ('id_tipo_vinculo', 'nombre')


class VinculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vinculo
        fields = ('id_vinculo', 'persona', 'persona_ep', 'tipo_vinculo')
        extra_kwargs = {'tipo_vinculo': {'allow_null': False, 'required': True}}
