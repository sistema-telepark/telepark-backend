from rest_framework import serializers
from core.fields import StrictBooleanField
from .models import (
    Taller, Encuentro, Actividad, EncuentroActividad,
    Asistenciataller, EncuentroFactorGlobal, Factorglobal,
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


class EncuentroActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncuentroActividad
        fields = ('idencuentroactividad', 'idactividad', 'idencuentro')


class AsistenciaTallerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistenciataller
        fields = ('idasistenciataller', 'estado', 'idpersonaep', 'idencuentro')
        extra_kwargs = {'idpersonaep': {'allow_null': True, 'required': False},
                        'idencuentro': {'allow_null': True, 'required': False}}


class EncuentroFactorGlobalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncuentroFactorGlobal
        fields = ('idencuentrofactorglobal', 'idencuentro', 'idfactorglobal')


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
        fields = ('idvariableuo', 'nombre', 'idunidadobservacion')


class ValorVariableUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valorvariableuo
        fields = ('idvalorvariableuo', 'valor', 'idvariableuo', 'idasistenciataller', 'idencuentroactividad')
        extra_kwargs = {'idasistenciataller': {'allow_null': True, 'required': False},
                        'idencuentroactividad': {'allow_null': True, 'required': False}}
