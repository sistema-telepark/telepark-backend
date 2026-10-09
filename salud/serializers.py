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
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Evolucion
        fields = ('id_evolucion', 'escala_evolucion', 'fecha', 'persona_ep', 'borrado')


class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('id_enfermedad', 'nombre')


class DiagnosticoSerializer(serializers.ModelSerializer):
    borrado = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Diagnostico
        fields = ('id_diagnostico', 'fecha', 'persona_ep', 'enfermedad', 'borrado')


class DiagnosticoEpSerializer(DiagnosticoSerializer):
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
    borrado = StrictBooleanField(required=False, default=False)
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
            'borrado',
        )


class IndicacionEpSerializer(IndicacionSerializer):
    medicamento = MedicamentoSerializer(many=False, read_only=True)

    class Meta(IndicacionSerializer.Meta):
        pass
