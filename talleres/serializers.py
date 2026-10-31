from rest_framework import serializers

from core.fields import StrictBooleanField
from core.serializers import StrictModelSerializer

from .models import (
    ESTADOS_ASISTENCIA,
    Actividad,
    AsistenciaTaller,
    Encuentro,
    EncuentroActividad,
    EncuentroFactorGlobal,
    EncuentroTaller,
    FactorGlobal,
    Taller,
    UnidadObservacion,
    ValorVariableUO,
    VariableUO,
)


class TallerSerializer(StrictModelSerializer):
    class Meta:
        model = Taller
        fields = ('id_taller', 'tipo_taller')


class EncuentroTallerSerializer(StrictModelSerializer):
    class Meta:
        model = EncuentroTaller
        fields = ('id_encuentro_taller', 'encuentro', 'taller')


class EncuentroSerializer(StrictModelSerializer):
    virtual = StrictBooleanField(required=False, default=False)
    talleres = EncuentroTallerSerializer(many=True, read_only=True)

    class Meta:
        model = Encuentro
        fields = ('id_encuentro', 'fecha', 'virtual', 'talleres')


class ActividadSerializer(StrictModelSerializer):
    class Meta:
        model = Actividad
        fields = ('id_actividad', 'nombre', 'taller')


class EncuentroActividadSerializer(StrictModelSerializer):
    class Meta:
        model = EncuentroActividad
        fields = ('id_encuentro_actividad', 'actividad', 'encuentro')


class AsistenciaTallerSerializer(StrictModelSerializer):
    estado = serializers.ChoiceField(choices=ESTADOS_ASISTENCIA, required=True)

    class Meta:
        model = AsistenciaTaller
        fields = ('id_asistencia_taller', 'estado', 'persona_ep', 'encuentro')
        validators = []


class RosterAsistenciaSerializer(serializers.Serializer):
    persona_ep = serializers.IntegerField()
    estado = serializers.CharField()


class EncuentroFactorGlobalSerializer(StrictModelSerializer):
    class Meta:
        model = EncuentroFactorGlobal
        fields = ('id_encuentro_factor_global', 'encuentro', 'factor_global')


class FactorGlobalSerializer(StrictModelSerializer):
    class Meta:
        model = FactorGlobal
        fields = ('id_factor_global', 'nombre')


class UnidadObservacionSerializer(StrictModelSerializer):
    class Meta:
        model = UnidadObservacion
        fields = ('id_unidad_observacion', 'nombre')


class VariableUOSerializer(StrictModelSerializer):
    class Meta:
        model = VariableUO
        fields = ('id_variable_uo', 'nombre', 'unidad_observacion')


class ValorVariableUOSerializer(StrictModelSerializer):
    class Meta:
        model = ValorVariableUO
        fields = ('id_valor_variable_uo', 'valor', 'variable_uo', 'asistencia_taller', 'encuentro_actividad')
        extra_kwargs = {
            'asistencia_taller': {'allow_null': True, 'required': False},
            'encuentro_actividad': {'allow_null': True, 'required': False},
        }
