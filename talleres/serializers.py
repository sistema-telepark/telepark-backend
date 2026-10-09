from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import (
    Actividad,
    AsistenciaTaller,
    Encuentro,
    EncuentroActividad,
    EncuentroFactorGlobal,
    FactorGlobal,
    Taller,
    UnidadObservacion,
    ValorVariableUO,
    VariableUO,
)


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ('id_taller', 'tipo_taller')


class EncuentroSerializer(serializers.ModelSerializer):
    virtual = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Encuentro
        fields = ('id_encuentro', 'fecha', 'virtual', 'taller')


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ('id_actividad', 'nombre', 'taller')


class EncuentroActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncuentroActividad
        fields = ('id_encuentro_actividad', 'actividad', 'encuentro')


class AsistenciaTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenciaTaller
        fields = ('id_asistencia_taller', 'estado', 'persona_ep', 'encuentro')
        extra_kwargs = {
            'persona_ep': {'allow_null': True, 'required': False},
            'encuentro': {'allow_null': True, 'required': False},
        }


class EncuentroFactorGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncuentroFactorGlobal
        fields = ('id_encuentro_factor_global', 'encuentro', 'factor_global')


class FactorGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactorGlobal
        fields = ('id_factor_global', 'nombre')


class UnidadObservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadObservacion
        fields = ('id_unidad_observacion', 'nombre')


class VariableUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableUO
        fields = ('id_variable_uo', 'nombre', 'unidad_observacion')


class ValorVariableUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValorVariableUO
        fields = ('id_valor_variable_uo', 'valor', 'variable_uo', 'asistencia_taller', 'encuentro_actividad')
        extra_kwargs = {
            'asistencia_taller': {'allow_null': True, 'required': False},
            'encuentro_actividad': {'allow_null': True, 'required': False},
        }
