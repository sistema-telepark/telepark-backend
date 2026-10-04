from django.db import models

from core.exceptions import ConflictError
from core.managers import OrdenadoManager


class AsistenciaTallerManager(OrdenadoManager):
    """Manager para Asistenciataller con orden compuesto."""

    def listar_ordenado(self):
        return self.all().order_by('idpersonaep', 'idasistenciataller')


class Taller(models.Model):
    idtaller = models.AutoField(db_column='idTaller', primary_key=True)
    tipotaller = models.CharField(db_column='tipoTaller', max_length=45)

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.encuentro_set.exists() or self.actividad_set.exists():
            raise ConflictError('No se puede eliminar un taller con encuentros o actividades asociados')

    class Meta:
        db_table = 'taller'


class Encuentro(models.Model):
    idencuentro = models.AutoField(db_column='idEncuentro', primary_key=True)
    fecha = models.DateField()
    virtual = models.BooleanField(db_column='virtual', default=False)
    idtaller = models.ForeignKey(Taller, models.PROTECT, db_column='idTaller')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'encuentro'


class Actividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)
    nombre = models.CharField(max_length=45)
    idtaller = models.ForeignKey(Taller, models.PROTECT, db_column='idTaller')

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.actividadrealizada_set.exists():
            raise ConflictError('No se puede eliminar una actividad con registros de actividades realizadas')

    class Meta:
        db_table = 'actividad'


class Actividadrealizada(models.Model):
    idactividadrealizada = models.AutoField(db_column='idActividadRealizada', primary_key=True)
    idactividad = models.ForeignKey(Actividad, models.PROTECT, db_column='idActividad')
    idencuentro = models.ForeignKey(Encuentro, models.CASCADE, db_column='idEncuentro')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'actividadrealizada'
        unique_together = (('idactividad', 'idencuentro'),)


class Asistenciataller(models.Model):
    idasistenciataller = models.AutoField(db_column='idAsistenciaTaller', primary_key=True)
    estado = models.CharField(max_length=45)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.PROTECT, db_column='idPersonaEP', blank=True, null=True)
    idencuentro = models.ForeignKey(Encuentro, models.SET_NULL, db_column='idEncuentro', blank=True, null=True)

    objects = AsistenciaTallerManager()

    class Meta:
        db_table = 'asistenciataller'


class Factorclase(models.Model):
    idfactorclase = models.AutoField(db_column='idFactorClase', primary_key=True)
    idencuentro = models.ForeignKey(Encuentro, models.CASCADE, db_column='idEncuentro')
    idfactorglobal = models.ForeignKey('Factorglobal', models.PROTECT, db_column='idFactorGlobal')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'factorclase'
        unique_together = (('idencuentro', 'idfactorglobal'),)


class Factorglobal(models.Model):
    idfactorglobal = models.AutoField(db_column='idFactorGlobal', primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'factorglobal'


class Unidadobservacion(models.Model):
    idunidadobservacion = models.AutoField(db_column='idUnidadObservacion', primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'unidadobservacion'


class Variableuo(models.Model):
    idvariableuo = models.AutoField(db_column='idVariableUO', primary_key=True)
    nombre = models.CharField(max_length=45)
    idunidadobservacion = models.ForeignKey(Unidadobservacion, models.PROTECT, db_column='idUnidadObservacion')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'variableuo'


class Valorvariableuo(models.Model):
    idvalorvariableuo = models.AutoField(db_column='idValorVariableUO', primary_key=True)
    valor = models.CharField(max_length=45)
    idvariableuo = models.ForeignKey(Variableuo, models.PROTECT, db_column='idVariableUO')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'valorvariableuo'
