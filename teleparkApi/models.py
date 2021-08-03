from django.db import models
from django.db.models.expressions import F

# Create your models here.
class Diagnostico(models.Model):
    idDiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)
    fecha = models.DateField()
    idPersona = models.ForeignKey('personaEp', models.DO_NOTHING, db_column='idPersona')
    idEnfermedad = models.ForeignKey('enfermedad', models.DO_NOTHING, db_column='idEnfermedad')

    class Meta:
        db_table = 'Diagnostico'

class Direccion(models.Model):
    idDireccion = models.AutoField(db_column='idDireccion', primary_key=True)
    calle = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    idLocalidad = models.ForeignKey('localidad', models.DO_NOTHING, db_column='idLocalidad', blank=True, null=True)

    class Meta:
        db_table = 'Direccion'

class Enfermedad(models.Model):
    idEnfermedad = models.IntegerField(db_column='idEnfermedad', primary_key=True)
    nombre = models.CharField(max_length=45)

    class Meta:
        db_table = 'Enfermedad'

class Localidad(models.Model):
    idLocalidad = models.AutoField(db_column='idLocalidad', primary_key=True)
    nombre = models.CharField(max_length=45)
    codigoPostal = models.IntegerField()
    idMunicipio = models.ForeignKey('municipio', models.DO_NOTHING, db_column='idMunicipio', blank=True, null=True)

    class Meta:
        db_table = 'Localidad'

class Municipio(models.Model):
    idMunicipio = models.AutoField(db_column='idMunicipio', primary_key=True)
    nombre = models.CharField(max_length=45)
    provincia = models.CharField(max_length=45)

    class Meta:
        db_table = 'Municipio'

class ObraSocial(models.Model):
    idObraSocial = models.AutoField(db_column='idObraSocial', primary_key=True)
    nombre = models.CharField(max_length=45)
    esEstatal = models.BooleanField(db_column='esEstatal')
    idPersonaEP = models.ForeignKey('personaEp', models.DO_NOTHING, db_column='idPersonaEP')

    class Meta:
        db_table = 'ObraSocial'

class Medicamento(models.Model):
    idMedicamento = models.AutoField(db_column='idMedicamento', primary_key=True)
    nombre = models.CharField(max_length=45)
    esAntiparkinsoniano = models.BooleanField(db_column='esAntiparkinsoniano')
    esLevodopa = models.BooleanField(db_column='esLevodopa')

    class Meta:
        db_table = 'Medicamento'


class Evolucion(models.Model):
    idEvolucion = models.AutoField(db_column='idEvolucion', primary_key=True)
    escalaEvolucion = models.BooleanField(db_column='escalaEvolucion')
    fecha = models.DateField(blank=True, null=True)
    idPersona = models.ForeignKey('personaEp', models.DO_NOTHING, db_column='idPersona')

    class Meta:
        db_table = 'Evolucion'


class IndicacionMedicamento(models.Model):
    idIndicacion = models.AutoField(db_column='idIndicacion', primary_key=True)
    cantidadMiligramos = models.IntegerField()
    estaVigente = models.BooleanField(null=True)
    fechaPrescripcion = models.DateField()
    horaDeToma = models.TimeField()
    idPersonaEP = models.ForeignKey('personaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idMedicamento = models.ForeignKey('medicamento', models.DO_NOTHING, db_column='idMedicamento')

    class Meta:
        db_table = 'IndicacionMedicamento'

class Persona(models.Model):
    SEXO = [
        ('M', 'Masculino'), 
        ('F', 'Femenino'),
        ('O', 'Otro')
    ]

    idPersona = models.AutoField(db_column='idPersona', primary_key=True)
    apellido = models.CharField(max_length=50, null=False)
    nombre = models.CharField(max_length=50, null=False)
    sexo=models.CharField(max_length=1, choices=SEXO, default='M', null=False)
    telefono=models.IntegerField(null=False)
    idDireccion = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='idDireccion', blank=True, null=True)
    
    class Meta:
        db_table = 'Persona'

class PersonaEP(Persona):
    TIPO_ESCOLARIDAD = [
        ('SIN_ESCOLARIDAD', 'Sin Escolaridad'),
        ('PRIMARIO', 'Primario'),
        ('SECUNDARIO', 'Secundario'),
        ('TERCIARIO', 'Terciario'),
        ('UNIVERSITARIO', 'Universitario')    
    ]

    idPersonaEP = models.AutoField(db_column='idPersonaEP', primary_key=True)
    escolaridadCompleta = models.BooleanField(default=False)
    fechaNacimiento = models.DateField(null=False)
    maximaEscolaridadAlcanzada = models.CharField(max_length=16, choices=TIPO_ESCOLARIDAD, default='SIN_ESCOLARIDAD')
    tieneAcompaniante = models.BooleanField(default=False, null=False)
    tieneCuidador = models.BooleanField(default=False, null=False)
    viveSolo = models.BooleanField(default=False, null=False)
    idReferente = models.ForeignKey(Persona, related_name='personaEpReferente', on_delete=models.PROTECT, db_column='idReferente', null=False)
    idOcupacionAnterior = models.ForeignKey(Persona, related_name='ocupacionAnterior', on_delete=models.PROTECT, db_column='idOcupacionAnterior', null=True)
    idOcupacionActual = models.ForeignKey(Persona, related_name='ocupacionActual', on_delete=models.PROTECT, db_column='idOcupacionActual', null=True)
    
    class Meta:
        db_table = 'PersonaEP'

class Evento(models.Model):
    fecha = models.DateField(null=False)
    motivo = models.CharField(max_length=100)
    idPersonaEP = models.ForeignKey(PersonaEP, related_name='eventoPersonaEP', db_column='idPersonaEP', on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = 'Evento'

class TipoEvento(models.Model):
    idTipoEvento = models.AutoField(db_column='idTipoEvento', primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'TipoEvento'


class TipoParentesco(models.Model):
    idTipoParentesco = models.AutoField(db_column='idTipoParentesco', primary_key=True)
    idPersona = models.OneToOneField(Persona, models.DO_NOTHING, db_column='idPersona', related_name='tipoParentescoPersona')
    idPersonaEP = models.ForeignKey(PersonaEP, models.DO_NOTHING, db_column='idPersonaEP', related_name='tipoParentescoPersonaEP')
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'TipoParentesco'
        unique_together = ('idPersona', 'idPersonaEP',)

class Ocupacion(models.Model):
    idOcupacion = models.AutoField(db_column='idOcupacion', primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'Ocupacion'