from core.fields import StrictBooleanField
from core.serializers import StrictModelSerializer

from .models import (
    Diagnostico,
    Enfermedad,
    Evolucion,
    IndicacionMedicamento,
    Medicamento,
)


class EvolucionSerializer(StrictModelSerializer):
    class Meta:
        model = Evolucion
        fields = ('id_evolucion', 'escala_evolucion', 'fecha', 'persona_ep')


class EnfermedadSerializer(StrictModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('id_enfermedad', 'nombre')


class DiagnosticoSerializer(StrictModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ('id_diagnostico', 'fecha', 'persona_ep', 'enfermedad')


class DiagnosticoEPSerializer(DiagnosticoSerializer):
    enfermedad = EnfermedadSerializer(many=False, read_only=True)

    class Meta(DiagnosticoSerializer.Meta):
        pass


class MedicamentoSerializer(StrictModelSerializer):
    es_antiparkinsoniano = StrictBooleanField(required=False, default=False)
    es_levodopa = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Medicamento
        fields = ('id_medicamento', 'nombre', 'es_antiparkinsoniano', 'es_levodopa')


class IndicacionSerializer(StrictModelSerializer):
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
