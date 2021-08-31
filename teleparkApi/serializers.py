#from backDjango.backTelepark.models import PersonaEp
from rest_framework import serializers
from rest_framework.utils import field_mapping 
from .models import Evento, Persona, Direccion, PersonaEp, Localidad, Municipio, Tipoevento, Tipoparentesco
 
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'localidad_idlocalidad')

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'direccion_iddireccion')

class PersonaEpSerializer(serializers.ModelSerializer):
    referente = PersonaSerializer()

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
                  'persona_idpersona',
                  'idreferente')

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = ('idlocalidad', 'nombre', 'codigopostal', 'municipio_idmunicipio')

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
