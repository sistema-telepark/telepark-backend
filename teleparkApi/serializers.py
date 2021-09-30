#from backDjango.backTelepark.models import PersonaEp
from rest_framework import serializers
from rest_framework.utils import field_mapping 
from .models import Evento, Enfermedad, Persona, Diagnostico, Direccion, PersonaEp, Localidad, Municipio, Tipoevento, Tipoparentesco

class DiagnosticoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnostico
        fields = ('iddiagnostico',
                  'fecha',
                  'idpersonaep',
                  'idenfermedad')

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'idlocalidad')

class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('idenfermedad', 'nombre')

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion')

class PersonaEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaEp
        fields = ('escolaridadcompleta',
                  'fechainicio',
                  'fechanacimiento',
                  'maximaescolaridadalcanzada',
                  'sexo',
                  'tieneacompanante',
                  'tienecuidador',
                  'vivesolo',
                  'ocupacionprevia',
                  'ocupacionactual',
                  'idpersona',
                  'idreferente')

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idlocalidad', 'nombre', 'codigopostal', 'idmunicipio')

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = ('idmunicipio', 'nombre', 'provincia')

class TipoparentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoparentesco
        fields = ('idpersona','idpersonaep','nombre')

class TipoEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoevento
        fields = ('idtipoevento', 'nombre')

class EventoSerializer(serializers.ModelSerializer):
    tipoEvento = TipoEventoSerializer

    class Meta:
        model = Evento
        fields = ('idevento','fecha','motivo')
