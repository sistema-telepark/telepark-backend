from rest_framework import serializers
from .models import (
    Diagnostico, Evolucion, Enfermedad,
    Medicamento, Indicacionmedicamento,
)


class EvolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evolucion
        fields = ('idevolucion', 'escalaevolucion', 'fecha', 'idpersonaep', 'borrado')


class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('idenfermedad', 'nombre')


class DiagnosticoEpSerializer(serializers.ModelSerializer):
    idenfermedad = EnfermedadSerializer(many=False, read_only=True)

    class Meta:
        model = Diagnostico
        fields = ('iddiagnostico',
                  'fecha',
                  'idpersonaep',
                  'idenfermedad',
                  'borrado')


class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ('iddiagnostico',
                  'fecha',
                  'idpersonaep',
                  'idenfermedad',
                  'borrado')


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ('idmedicamento', 'nombre', 'esantiparkinsoniano', 'eslevodopa')


class IndicacionEpSerializer(serializers.ModelSerializer):
    idmedicamento = MedicamentoSerializer(many=False, read_only=True)

    class Meta:
        model = Indicacionmedicamento
        fields = ('idindicacion',
                  'cantidadmiligramos',
                  'estavigente',
                  'fechaprescripcion',
                  'horadetoma',
                  'idpersonaep',
                  'idmedicamento',
                  'borrado')


class IndicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicacionmedicamento
        fields = ('idindicacion',
                  'cantidadmiligramos',
                  'estavigente',
                  'fechaprescripcion',
                  'horadetoma',
                  'idpersonaep',
                  'idmedicamento',
                  'borrado')
