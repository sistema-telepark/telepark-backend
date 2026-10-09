from django.db import models

from core.managers import OrdenadoManager

from .managers import NombreOrderedManager


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=35)
    direccion = models.ForeignKey('Direccion', models.DO_NOTHING, blank=True, null=True)
    borrado = models.BooleanField(default=False)
    sexo = models.CharField(max_length=45, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'personas_persona'


class PersonaEP(Persona):
    persona_ptr = models.OneToOneField(
        Persona, models.DO_NOTHING, db_column='id_persona', parent_link=True, primary_key=True
    )
    activa_taller = models.BooleanField(default=False)
    escolaridad_completa = models.BooleanField(default=False)
    fecha_inicio = models.DateTimeField()
    maxima_escolaridad_alcanzada = models.CharField(max_length=45, blank=True, null=True)
    tiene_acompanante = models.BooleanField(default=False)
    tiene_cuidador = models.BooleanField(default=False)
    vive_solo = models.BooleanField(default=False)
    ocupacion_previa = models.CharField(max_length=45)
    ocupacion_actual = models.CharField(max_length=45)
    referente = models.ForeignKey(Persona, models.DO_NOTHING, related_name='+')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'personas_persona_ep'


class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    localidad = models.ForeignKey('Localidad', models.DO_NOTHING, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'personas_direccion'


class Localidad(models.Model):
    id_localidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    codigo_postal = models.IntegerField(null=True, blank=True)
    departamento = models.ForeignKey('Departamento', models.DO_NOTHING, blank=True, null=True)

    objects = NombreOrderedManager()

    class Meta:
        db_table = 'personas_localidad'
        ordering = ('nombre',)


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    objects = NombreOrderedManager()

    class Meta:
        db_table = 'personas_provincia'
        ordering = ('nombre',)


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, blank=True, null=True)

    objects = NombreOrderedManager()

    class Meta:
        db_table = 'personas_departamento'
        ordering = ('nombre',)


class TipoParentesco(models.Model):
    id_tipo_parentesco = models.AutoField(primary_key=True)
    persona = models.ForeignKey(Persona, models.DO_NOTHING)
    persona_ep = models.ForeignKey(PersonaEP, models.DO_NOTHING, related_name='+')
    nombre = models.CharField(max_length=45, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'personas_tipo_parentesco'
        unique_together = (('persona', 'persona_ep'),)
