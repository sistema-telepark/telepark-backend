from rest_framework import serializers

from core.fields import StrictBooleanField

from .models import (
    Diagnostico,
    Enfermedad,
    Evolucion,
    IndicacionMedicamento,
    Medicamento,
)


class EvolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evolucion
        fields = ('id_evolucion', 'escala_evolucion', 'fecha', 'persona_ep')


class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('id_enfermedad', 'nombre')


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ('id_diagnostico', 'fecha', 'persona_ep', 'enfermedad')


class DiagnosticoEPSerializer(DiagnosticoSerializer):
    enfermedad = EnfermedadSerializer(many=False, read_only=True)

    class Meta(DiagnosticoSerializer.Meta):
        pass


class MedicamentoSerializer(serializers.ModelSerializer):
    es_antiparkinsoniano = StrictBooleanField(required=False, default=False)
    es_levodopa = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Medicamento
        fields = ('id_medicamento', 'nombre', 'es_antiparkinsoniano', 'es_levodopa')


class IndicacionSerializer(serializers.ModelSerializer):
    esta_vigente = StrictBooleanField(required=False, default=False)

    class Meta:
        model = IndicacionMedicamento
        fields = (
            'id_indicacion',
            'cantidad_miligramos',
            'esta_vigente',
            'fecha_prescripcion',
            'hora_de_toma',
            'persona_ep',
            'medicamento',
        )


class IndicacionEPSerializer(IndicacionSerializer):
    medicamento = MedicamentoSerializer(many=False, read_only=True)

    class Meta(IndicacionSerializer.Meta):
        pass
