# This is an auto-generated Django model module — cleaned.
# Todos los modelos tienen managed=True (por defecto, sin declaración explícita).
# Django administra el ciclo de vida de estas tablas vía migraciones.
# Los modelos del framework Django (Auth*, Django*) fueron eliminados porque
# ya son gestionados por django.contrib.auth, django.contrib.contenttypes, etc.
from django.db import models


class Actividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    idtaller = models.ForeignKey('Taller', models.DO_NOTHING, db_column='idTaller')  # Field name made lowercase.

    class Meta:
        db_table = 'actividad'


class Actividadrealizada(models.Model):
    idactividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='idActividad', primary_key=True)  # Field name made lowercase.
    idclasetaller = models.ForeignKey('Clasetaller', models.DO_NOTHING, db_column='idClaseTaller')  # Field name made lowercase.

    class Meta:
        db_table = 'actividadrealizada'
        unique_together = (('idactividad', 'idclasetaller'),)


class Asistenciataller(models.Model):
    idasistenciataller = models.AutoField(db_column='idAsistenciaTaller', primary_key=True)  # Field name made lowercase.
    estado = models.CharField(max_length=45)
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idclasetaller = models.ForeignKey('Clasetaller', models.DO_NOTHING, db_column='idClaseTaller')  # Field name made lowercase.
    idcomportamiento = models.ForeignKey('Comportamiento', models.DO_NOTHING, db_column='idComportamiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'asistenciataller'


class Clasetaller(models.Model):
    idclasetaller = models.AutoField(db_column='idClaseTaller', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    virtual = models.IntegerField()
    idtaller = models.ForeignKey('Taller', models.DO_NOTHING, db_column='idTaller')  # Field name made lowercase.

    class Meta:
        db_table = 'clasetaller'


class Comportamiento(models.Model):
    idcomportamiento = models.AutoField(db_column='idComportamiento', primary_key=True)  # Field name made lowercase.
    comentario = models.CharField(max_length=45)

    class Meta:
        db_table = 'comportamiento'


class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idenfermedad = models.ForeignKey('Enfermedad', models.DO_NOTHING, db_column='idEnfermedad')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        db_table = 'diagnostico'


class Direccion(models.Model):
    iddireccion = models.AutoField(db_column='idDireccion', primary_key=True)  # Field name made lowercase.
    calle = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    idlocalidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='idLocalidad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'direccion'


class Enfermedad(models.Model):
    idenfermedad = models.AutoField(db_column='idEnfermedad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        db_table = 'enfermedad'


class Evento(models.Model):
    idevento = models.AutoField(db_column='idEvento', primary_key=True)  # Field name made lowercase.
    fechadesde = models.DateField(db_column='fechaDesde', blank=True, null=True)
    fechahasta = models.DateField(db_column='fechaHasta', blank=True, null=True)
    motivo = models.CharField(max_length=256, blank=True, null=True)
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idtipoevento = models.ForeignKey('Tipoevento', models.DO_NOTHING, db_column='idTipoEvento')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        db_table = 'evento'


class Evolucion(models.Model):
    idevolucion = models.AutoField(db_column='idEvolucion', primary_key=True)  # Field name made lowercase.
    escalaevolucion = models.IntegerField(db_column='escalaEvolucion')  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.
    class Meta:
        db_table = 'evolucion'


class Factorclase(models.Model):
    idclasetaller = models.OneToOneField(Clasetaller, models.DO_NOTHING, db_column='idClaseTaller', primary_key=True)  # Field name made lowercase.
    idfactorglobal = models.ForeignKey('Factorglobal', models.DO_NOTHING, db_column='idFactorGlobal')  # Field name made lowercase.

    class Meta:
        db_table = 'factorclase'
        unique_together = (('idclasetaller', 'idfactorglobal'),)


class Factorglobal(models.Model):
    idfactorglobal = models.AutoField(db_column='idFactorGlobal', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        db_table = 'factorglobal'


class Indicacionmedicamento(models.Model):
    idindicacion = models.AutoField(db_column='idIndicacion', primary_key=True)  # Field name made lowercase.
    cantidadmiligramos = models.IntegerField(db_column='cantidadMiligramos', blank=True, null=True)  # Field name made lowercase.
    estavigente = models.IntegerField(db_column='estaVigente', blank=True, null=True)  # Field name made lowercase.
    fechaprescripcion = models.DateField(db_column='fechaPrescripcion', blank=True, null=True)  # Field name made lowercase.
    horadetoma = models.TimeField(db_column='horaDeToma', blank=True, null=True)  # Field name made lowercase.
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idmedicamento = models.ForeignKey('Medicamento', models.DO_NOTHING, db_column='idMedicamento')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        db_table = 'indicacionmedicamento'


class Localidad(models.Model):
    idlocalidad = models.AutoField(db_column='idLocalidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    codigopostal = models.IntegerField(db_column='codigoPostal')  # Field name made lowercase.
    idmunicipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='idMunicipio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'localidad'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(db_column='idMedicamento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    esantiparkinsoniano = models.IntegerField(db_column='esAntiparkinsoniano', blank=True, null=True)  # Field name made lowercase.
    eslevodopa = models.IntegerField(db_column='esLevodopa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'medicamento'


class Municipio(models.Model):
    idmunicipio = models.AutoField(db_column='idMunicipio', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    provincia = models.CharField(max_length=45)

    class Meta:
        db_table = 'municipio'


class Obrasocial(models.Model):
    idobrasocial = models.AutoField(db_column='idObraSocial', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    esestatal = models.IntegerField(db_column='esEstatal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'obrasocial'


class Os(models.Model):
    idos = models.AutoField(db_column='idOS', primary_key=True)  # Field name made lowercase.
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idobrasocial = models.ForeignKey('Obrasocial', models.DO_NOTHING, db_column='idObraSocial')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        db_table = 'os'


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=35)
    iddireccion = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='idDireccion', blank=True, null=True)  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.
    espaciente = models.IntegerField(db_column='esPaciente')  # Field name made lowercase.

    class Meta:
        db_table = 'persona'


class PersonaEp(models.Model):
    activataller = models.IntegerField(db_column='activaTaller', blank=True, null=True)  # Field name made lowercase.
    escolaridadcompleta = models.IntegerField(db_column='escolaridadCompleta', blank=True, null=True)  # Field name made lowercase.
    fechainicio = models.DateTimeField(db_column='fechaInicio')  # Field name made lowercase.
    fechanacimiento = models.DateField(db_column='fechaNacimiento')  # Field name made lowercase.
    maximaescolaridadalcanzada = models.CharField(db_column='maximaEscolaridadAlcanzada', max_length=45, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(max_length=45)
    tieneacompanante = models.IntegerField(db_column='tieneAcompanante')  # Field name made lowercase.
    tienecuidador = models.IntegerField(db_column='tieneCuidador')  # Field name made lowercase.
    vivesolo = models.IntegerField(db_column='viveSolo')  # Field name made lowercase.
    ocupacionprevia = models.CharField(db_column='ocupacionPrevia', max_length=45)  # Field name made lowercase.
    ocupacionactual = models.CharField(db_column='ocupacionActual', max_length=45)  # Field name made lowercase.
    idpersona = models.OneToOneField(Persona, models.DO_NOTHING, db_column='idPersona', primary_key=True)  # Field name made lowercase.
    idreferente = models.ForeignKey(Persona, models.DO_NOTHING, db_column='idReferente', related_name='+')  # Field name made lowercase.

    class Meta:
        db_table = 'persona_ep'
        unique_together = (('idpersona', 'idreferente'),)


class Taller(models.Model):
    idtaller = models.AutoField(db_column='idTaller', primary_key=True)  # Field name made lowercase.
    tipotaller = models.CharField(db_column='tipoTaller', max_length=45)  # Field name made lowercase.

    class Meta:
        db_table = 'taller'


class Tipoevento(models.Model):
    idtipoevento = models.AutoField(db_column='idTipoEvento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    desactivataller = models.IntegerField(db_column='desactivaTaller', blank=True, null=True)  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        db_table = 'tipoevento'


class Tipoparentesco(models.Model):
    idpersona = models.OneToOneField(Persona, models.DO_NOTHING, db_column='idPersona', primary_key=True)  # Field name made lowercase.
    idpersonaep = models.ForeignKey(PersonaEp, models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'tipoparentesco'
        unique_together = (('idpersona', 'idpersonaep'),)


class Unidadobservacion(models.Model):
    idunidadobservacion = models.AutoField(db_column='idUnidadObservacion', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        db_table = 'unidadobservacion'


class Valorvariableuo(models.Model):
    idvalorvariableuo = models.AutoField(db_column='idValorVariableUO', primary_key=True)  # Field name made lowercase.
    valor = models.CharField(max_length=45)
    idvariableuo = models.ForeignKey('Variableuo', models.DO_NOTHING, db_column='idVariableUO')  # Field name made lowercase.

    class Meta:
        db_table = 'valorvariableuo'


class Variableuo(models.Model):
    idvariableuo = models.AutoField(db_column='idVariableUO', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    idcomportamiento = models.ForeignKey(Comportamiento, models.DO_NOTHING, db_column='idComportamiento')  # Field name made lowercase.
    idunidadobservacion = models.ForeignKey(Unidadobservacion, models.DO_NOTHING, db_column='idUnidadObservacion')  # Field name made lowercase.

    class Meta:
        db_table = 'variableuo'

