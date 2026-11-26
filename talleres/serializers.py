from rest_framework import serializers

from core.fields import StrictBooleanField
from core.serializers import StrictModelSerializer

from .models import (
    ESTADOS_ASISTENCIA,
    Actividad,
    AsistenciaEncuentro,
    Encuentro,
    EncuentroFactorGlobal,
    EncuentroTaller,
    EncuentroTallerActividad,
    FactorGlobal,
    Taller,
    UnidadObservacion,
    ValorVariableUO,
    VariableUO,
)


class TallerSerializer(StrictModelSerializer):
    class Meta:
        model = Taller
        fields = ('id_taller', 'nombre')


class ActividadSerializer(StrictModelSerializer):
    class Meta:
        model = Actividad
        fields = ('id_actividad', 'nombre', 'taller')


class EncuentroTallerActividadSerializer(StrictModelSerializer):
    class Meta:
        model = EncuentroTallerActividad
        fields = ('id_encuentro_taller_actividad', 'encuentro_taller', 'actividad')

    def validate(self, attrs):
        actividad = attrs.get('actividad', getattr(self.instance, 'actividad', None))
        encuentro_taller = attrs.get('encuentro_taller', getattr(self.instance, 'encuentro_taller', None))
        if actividad is not None and encuentro_taller is not None:
            EncuentroTallerActividad.validar_actividad(actividad, encuentro_taller)
        return attrs


class EncuentroTallerSerializer(StrictModelSerializer):
    actividades_realizadas = EncuentroTallerActividadSerializer(many=True, read_only=True)

    class Meta:
        model = EncuentroTaller
        fields = ('id_encuentro_taller', 'encuentro', 'taller', 'actividades_realizadas')


class EncuentroSerializer(StrictModelSerializer):
    virtual = StrictBooleanField(required=False, default=False)
    talleres = EncuentroTallerSerializer(many=True, read_only=True)

    class Meta:
        model = Encuentro
        fields = ('id_encuentro', 'fecha', 'virtual', 'talleres')


class AsistenciaEncuentroSerializer(StrictModelSerializer):
    estado = serializers.ChoiceField(choices=ESTADOS_ASISTENCIA, required=True)

    class Meta:
        model = AsistenciaEncuentro
        fields = ('id_asistencia_encuentro', 'estado', 'persona_ep', 'encuentro')
        validators = []


class RosterAsistenciaSerializer(serializers.Serializer):
    persona_ep = serializers.IntegerField()
    estado = serializers.CharField()
    justificada = serializers.BooleanField(
        help_text='True solo cuando el estado es "Ausente" y un evento de la persona cubre la fecha del encuentro.'
    )


class ReporteEncuentroSerializer(serializers.Serializer):
    encuentro = serializers.IntegerField()
    fecha = serializers.DateField()
    estado = serializers.CharField()
    justificada = serializers.BooleanField()


class ReporteFaltasConsecutivasSerializer(serializers.Serializer):
    persona_ep = serializers.IntegerField()
    encuentros = ReporteEncuentroSerializer(many=True)


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
        fields = (
            'id_valor_variable_uo',
            'valor',
            'variable_uo',
            'asistencia_encuentro',
            'encuentro_taller_actividad',
        )
        extra_kwargs = {
            'asistencia_encuentro': {'allow_null': True, 'required': False},
            'encuentro_taller_actividad': {'allow_null': True, 'required': False},
        }
