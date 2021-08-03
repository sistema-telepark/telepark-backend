from rest_framework import serializers
from .models import Direccion, Evento, Localidad, Municipio, Ocupacion, Persona, PersonaEP, TipoParentesco

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['idDireccion', 'calle', 'departamento', 'numero', 'piso', 'idLocalidad']

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idLocalidad', 'nombre', 'codigoPostal', 'idMunicipio')

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('idMunicipio', 'nombre', 'provincia')

class TipoParentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoParentesco
        fields = ('idPersona', 'idPersonaEP', 'nombre')

class OcupacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocupacion
        fields = ('idOcupacion', 'nombre')

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['idPersona', 'apellido', 'nombre', 'sexo', 'telefono', 'idDireccion']

class PersonaEPSerializer(serializers.ModelSerializer):
    referente = PersonaSerializer()

    class Meta:
        model = PersonaEP
        fields = ['idPersonaEP', 'apellido', 'nombre', 'sexo', 'telefono', 'fechaNacimiento', 'escolaridadCompleta', 'maximaEscolaridadAlcanzada', 'tieneAcompaniante', 'tieneCuidador', 'viveSolo', 'idReferente']

class EventoSerializer(serializers.ModelSerializer):
    personaEp = PersonaEPSerializer()

    class Meta:
        model = Evento
        fields = ['idEvento', 'fecha', 'motivo', 'personaEp']