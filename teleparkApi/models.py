# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    idtaller = models.ForeignKey('Taller', models.DO_NOTHING, db_column='idTaller')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actividad'


class Actividadrealizada(models.Model):
    idactividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='idActividad', primary_key=True)  # Field name made lowercase.
    idclasetaller = models.ForeignKey('Clasetaller', models.DO_NOTHING, db_column='idClaseTaller')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'actividadrealizada'
        unique_together = (('idactividad', 'idclasetaller'),)


class Asistenciataller(models.Model):
    idasistenciataller = models.AutoField(db_column='idAsistenciaTaller', primary_key=True)  # Field name made lowercase.
    estado = models.CharField(max_length=45)
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idclasetaller = models.ForeignKey('Clasetaller', models.DO_NOTHING, db_column='idClaseTaller')  # Field name made lowercase.
    idcomportamiento = models.ForeignKey('Comportamiento', models.DO_NOTHING, db_column='idComportamiento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'asistenciataller'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Clasetaller(models.Model):
    idclasetaller = models.AutoField(db_column='idClaseTaller', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    virtual = models.IntegerField()
    idtaller = models.ForeignKey('Taller', models.DO_NOTHING, db_column='idTaller')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'clasetaller'


class Comportamiento(models.Model):
    idcomportamiento = models.AutoField(db_column='idComportamiento', primary_key=True)  # Field name made lowercase.
    comentario = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'comportamiento'


class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)  # Field name made lowercase.
    fecha = models.DateField()
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idenfermedad = models.ForeignKey('Enfermedad', models.DO_NOTHING, db_column='idEnfermedad')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'diagnostico'


class Direccion(models.Model):
    iddireccion = models.AutoField(db_column='idDireccion', primary_key=True)  # Field name made lowercase.
    calle = models.CharField(max_length=45, blank=True, null=True)
    departamento = models.CharField(max_length=45, blank=True, null=True)
    numero = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    idlocalidad = models.ForeignKey('Localidad', models.DO_NOTHING, db_column='idLocalidad', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'direccion'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Enfermedad(models.Model):
    idenfermedad = models.AutoField(db_column='idEnfermedad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'evento'


class Evolucion(models.Model):
    idevolucion = models.AutoField(db_column='idEvolucion', primary_key=True)  # Field name made lowercase.
    escalaevolucion = models.IntegerField(db_column='escalaEvolucion')  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'evolucion'


class Factorclase(models.Model):
    idclasetaller = models.OneToOneField(Clasetaller, models.DO_NOTHING, db_column='idClaseTaller', primary_key=True)  # Field name made lowercase.
    idfactorglobal = models.ForeignKey('Factorglobal', models.DO_NOTHING, db_column='idFactorGlobal')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'factorclase'
        unique_together = (('idclasetaller', 'idfactorglobal'),)


class Factorglobal(models.Model):
    idfactorglobal = models.AutoField(db_column='idFactorGlobal', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'indicacionmedicamento'


class Localidad(models.Model):
    idlocalidad = models.AutoField(db_column='idLocalidad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    codigopostal = models.IntegerField(db_column='codigoPostal')  # Field name made lowercase.
    idmunicipio = models.ForeignKey('Municipio', models.DO_NOTHING, db_column='idMunicipio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'localidad'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(db_column='idMedicamento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    esantiparkinsoniano = models.IntegerField(db_column='esAntiparkinsoniano', blank=True, null=True)  # Field name made lowercase.
    eslevodopa = models.IntegerField(db_column='esLevodopa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medicamento'


class Municipio(models.Model):
    idmunicipio = models.AutoField(db_column='idMunicipio', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    provincia = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'municipio'


class Obrasocial(models.Model):
    idobrasocial = models.AutoField(db_column='idObraSocial', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    esestatal = models.IntegerField(db_column='esEstatal', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'obrasocial'


class Os(models.Model):
    idos = models.AutoField(db_column='idOS', primary_key=True)  # Field name made lowercase.
    idpersonaep = models.ForeignKey('PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    idobrasocial = models.ForeignKey('Obrasocial', models.DO_NOTHING, db_column='idObraSocial')  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'os'


class Persona(models.Model):
    idpersona = models.AutoField(db_column='idPersona', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    telefono = models.CharField(max_length=35)
    iddireccion = models.ForeignKey(Direccion, models.DO_NOTHING, db_column='idDireccion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
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
        managed = False
        db_table = 'persona_ep'
        unique_together = (('idpersona', 'idreferente'),)


class Taller(models.Model):
    idtaller = models.AutoField(db_column='idTaller', primary_key=True)  # Field name made lowercase.
    tipotaller = models.CharField(db_column='tipoTaller', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'taller'


class Tipoevento(models.Model):
    idtipoevento = models.AutoField(db_column='idTipoEvento', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)
    desactivataller = models.IntegerField(db_column='desactivaTaller', blank=True, null=True)  # Field name made lowercase.
    borrado = models.IntegerField(db_column='borrado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tipoevento'


class Tipoparentesco(models.Model):
    idpersona = models.OneToOneField(Persona, models.DO_NOTHING, db_column='idPersona', primary_key=True)  # Field name made lowercase.
    idpersonaep = models.ForeignKey(PersonaEp, models.DO_NOTHING, db_column='idPersonaEP')  # Field name made lowercase.
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipoparentesco'
        unique_together = (('idpersona', 'idpersonaep'),)


class Unidadobservacion(models.Model):
    idunidadobservacion = models.AutoField(db_column='idUnidadObservacion', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'unidadobservacion'


class Valorvariableuo(models.Model):
    idvalorvariableuo = models.AutoField(db_column='idValorVariableUO', primary_key=True)  # Field name made lowercase.
    valor = models.CharField(max_length=45)
    idvariableuo = models.ForeignKey('Variableuo', models.DO_NOTHING, db_column='idVariableUO')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'valorvariableuo'


class Variableuo(models.Model):
    idvariableuo = models.AutoField(db_column='idVariableUO', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=45)
    idcomportamiento = models.ForeignKey(Comportamiento, models.DO_NOTHING, db_column='idComportamiento')  # Field name made lowercase.
    idunidadobservacion = models.ForeignKey(Unidadobservacion, models.DO_NOTHING, db_column='idUnidadObservacion')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'variableuo'
