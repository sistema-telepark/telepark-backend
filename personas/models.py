from django.db import models

from core.managers import OrdenadoManager


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=35)
    iddireccion = models.ForeignKey('Direccion', models.DO_NOTHING, db_column='idDireccion', blank=True, null=True)
    borrado = models.BooleanField(db_column='borrado', default=False)
    sexo = models.CharField(max_length=45, blank=True, null=True)
    fechanacimiento = models.DateField(db_column='fechaNacimiento', blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'persona'


class PersonaEp(Persona):
    persona_ptr = models.OneToOneField(
        Persona, models.DO_NOTHING, db_column='idPersona',
        parent_link=True, primary_key=True
    )
    activataller = models.IntegerField(db_column='activaTaller', blank=True, null=True)
    escolaridadcompleta = models.IntegerField(db_column='escolaridadCompleta', blank=True, null=True)
    fechainicio = models.DateTimeField(db_column='fechaInicio')
    maximaescolaridadalcanzada = models.CharField(db_column='maximaEscolaridadAlcanzada', max_length=45, blank=True, null=True)
    tieneacompanante = models.IntegerField(db_column='tieneAcompanante')
    tienecuidador = models.IntegerField(db_column='tieneCuidador')
    vivesolo = models.IntegerField(db_column='viveSolo')
    ocupacionprevia = models.CharField(db_column='ocupacionPrevia', max_length=45)
    ocupacionactual = models.CharField(db_column='ocupacionActual', max_length=45)
    idreferente = models.ForeignKey(
        Persona, models.DO_NOTHING, db_column='idReferente', related_name='+'
    )

    objects = OrdenadoManager()

    class Meta:
        db_table = 'persona_ep'


class Direccion(models.Model):
    iddireccion = models.AutoField(db_column='idDireccion', primary_key=True)
    calle = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    idlocalidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='idLocalidad', blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'direccion'


class Localidad(models.Model):
    idlocalidad = models.AutoField(db_column='idLocalidad', primary_key=True)
    nombre = models.CharField(max_length=120)
    codigopostal = models.IntegerField(db_column='codigoPostal', null=True, blank=True)
    idmunicipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='idMunicipio', blank=True, null=True)
    id_georef = models.CharField(db_column='idGeoref', unique=True, null=True, blank=True, max_length=20)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'localidad'


class Provincia(models.Model):
    idprovincia = models.AutoField(db_column='idProvincia', primary_key=True)
    nombre = models.CharField(max_length=100)
    id_georef = models.CharField(db_column='idGeoref', unique=True, null=True, blank=True, max_length=20)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'provincia'


class Municipio(models.Model):
    idmunicipio = models.AutoField(db_column='idMunicipio', primary_key=True)
    nombre = models.CharField(max_length=120)
    idprovincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='idProvincia', blank=True, null=True)
    id_georef = models.CharField(db_column='idGeoref', unique=True, null=True, blank=True, max_length=20)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'municipio'


class Tipoparentesco(models.Model):
    idtipoparentesco = models.AutoField(db_column='idTipoParentesco', primary_key=True)
    idpersona = models.ForeignKey(Persona, models.DO_NOTHING, db_column='idPersona')
    idpersonaep = models.ForeignKey(PersonaEp, models.DO_NOTHING, db_column='idPersonaEP', related_name='+')
    nombre = models.CharField(max_length=45, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'tipoparentesco'
        unique_together = (('idpersona', 'idpersonaep'),)
