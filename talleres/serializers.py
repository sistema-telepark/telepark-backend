from rest_framework import serializers
from core.fields import StrictBooleanField
from .models import (
    Taller, Encuentro, Actividad, Actividadrealizada,
    Asistenciataller, Comportamiento, Factorclase, Factorglobal,
    Unidadobservacion, Variableuo, Valorvariableuo,
)


class TallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taller
        fields = ('idtaller', 'tipotaller')


class EncuentroSerializer(serializers.ModelSerializer):
    virtual = StrictBooleanField(required=False, default=False)

    class Meta:
        model = Encuentro
        fields = ('idencuentro', 'fecha', 'virtual', 'idtaller')


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ('idactividad', 'nombre', 'idtaller')


class ActividadRealizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividadrealizada
        fields = ('idactividad', 'idencuentro')


class ComportamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comportamiento
        fields = ('idcomportamiento', 'comentario')


class AsistenciaTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistenciataller
        fields = ('idasistenciataller', 'estado', 'idpersonaep', 'idencuentro', 'idcomportamiento')
        extra_kwargs = {'idcomportamiento': {'allow_null': True, 'required': False},
                        'idpersonaep': {'allow_null': True, 'required': False},
                        'idencuentro': {'allow_null': True, 'required': False}}


class FactorClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factorclase
        fields = ('idencuentro', 'idfactorglobal')


class FactorGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factorglobal
        fields = ('idfactorglobal', 'nombre')


class UnidadObservacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidadobservacion
        fields = ('idunidadobservacion', 'nombre')


class VariableUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variableuo
        fields = ('idvariableuo', 'nombre', 'idcomportamiento', 'idunidadobservacion')


class ValorVariableUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valorvariableuo
        fields = ('idvalorvariableuo', 'valor', 'idvariableuo')
