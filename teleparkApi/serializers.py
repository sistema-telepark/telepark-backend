#from backDjango.backTelepark.models import PersonaEp
from rest_framework import serializers
from rest_framework.utils import field_mapping 
from .models import Evento, Evolucion, Enfermedad, Indicacionmedicamento, Medicamento, Persona, Diagnostico, Direccion, PersonaEp, Localidad, Municipio, Tipoevento, Tipoparentesco, Obrasocial, Os

class EvolucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evolucion
        fields = ('idevolucion', 'escalaevolucion', 'fecha', 'idpersonaep', 'borrado')

class EnfermedadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfermedad
        fields = ('idenfermedad', 'nombre')

class DiagnosticoEpSerializer(serializers.ModelSerializer):
    idenfermedad = EnfermedadSerializer(many= False, read_only=True)
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

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('iddireccion',
                  'calle',
                  'departamento',
                  'numero',
                  'piso',
                  'idlocalidad')

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('idpersona', 'nombre', 'apellido', 'telefono', 'iddireccion', 'borrado', 'espaciente')

class PersonaEpSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaEp
        fields = ('activataller',
                  'escolaridadcompleta',
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


class PersonaPSerializer(serializers.ModelSerializer):
    idpersona = PersonaSerializer(many= False, read_only=True)
    class Meta:
        model = PersonaEp
        fields = ('sexo','idpersona')

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
        fields = ('idtipoevento', 'nombre', 'desactivataller', 'borrado')

class EventoSerializer(serializers.ModelSerializer):
    tipoEvento = TipoEventoSerializer(many=False, read_only=True)

    class Meta:
        model = Evento
        fields = ('idevento','fechadesde', 'fechahasta', 'motivo', 'idpersonaep', 'idtipoevento', 'tipoEvento', 'borrado')

class ObraSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obrasocial
        fields = ('idobrasocial', 'nombre', 'esestatal')


class OSEpSerializer(serializers.ModelSerializer):
    idobrasocial = ObraSocialSerializer(many= False, read_only=True)
    class Meta:
        model = Os
        fields = ('idos', 'idpersonaep', 'idobrasocial', 'borrado')

class OSSerializer(serializers.ModelSerializer):
    class Meta:
        model = Os
        fields = ('idos', 'idpersonaep', 'idobrasocial', 'borrado')

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ('idmedicamento', 'nombre', 'esantiparkinsoniano', 'eslevodopa')

class IndicacionEpSerializer(serializers.ModelSerializer):
    idmedicamento = MedicamentoSerializer(many= False, read_only=True)
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