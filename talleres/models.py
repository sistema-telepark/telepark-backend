from django.db import models

from core.managers import OrdenadoManager


class TallerManager(OrdenadoManager):
    """Manager para Taller con orden por PK."""


class ClaseTallerManager(OrdenadoManager):
    """Manager para Clasetaller con orden por PK."""


class ActividadManager(OrdenadoManager):
    """Manager para Actividad con orden por PK."""


class ActividadRealizadaManager(OrdenadoManager):
    """Manager para Actividadrealizada con orden por PK."""


class AsistenciaTallerManager(OrdenadoManager):
    """Manager para Asistenciataller con orden compuesto."""

    def listar_ordenado(self):
        return self.all().order_by('idpersonaep', 'idasistenciataller')


class ComportamientoManager(OrdenadoManager):
    """Manager para Comportamiento con orden por PK."""


class FactorClaseManager(OrdenadoManager):
    """Manager para Factorclase con orden por PK."""


class FactorGlobalManager(OrdenadoManager):
    """Manager para Factorglobal con orden por PK."""


class UnidadObservacionManager(OrdenadoManager):
    """Manager para Unidadobservacion con orden por PK."""


class VariableUOManager(OrdenadoManager):
    """Manager para Variableuo con orden por PK."""


class ValorVariableUOManager(OrdenadoManager):
    """Manager para Valorvariableuo con orden por PK."""


class Taller(models.Model):
    idtaller = models.AutoField(db_column='idTaller', primary_key=True)
    tipotaller = models.CharField(db_column='tipoTaller', max_length=45)

    objects = TallerManager()

    class Meta:
        db_table = 'taller'


class Clasetaller(models.Model):
    idclasetaller = models.AutoField(db_column='idClaseTaller', primary_key=True)
    fecha = models.DateField()
    virtual = models.IntegerField()
    idtaller = models.ForeignKey(Taller, models.DO_NOTHING, db_column='idTaller')

    objects = ClaseTallerManager()

    class Meta:
        db_table = 'clasetaller'


class Actividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)
    nombre = models.CharField(max_length=45)
    idtaller = models.ForeignKey(Taller, models.DO_NOTHING, db_column='idTaller')

    objects = ActividadManager()

    class Meta:
        db_table = 'actividad'


class Actividadrealizada(models.Model):
    idactividad = models.OneToOneField(Actividad, models.DO_NOTHING, db_column='idActividad', primary_key=True)
    idclasetaller = models.ForeignKey(Clasetaller, models.DO_NOTHING, db_column='idClaseTaller')

    objects = ActividadRealizadaManager()

    class Meta:
        db_table = 'actividadrealizada'
        unique_together = (('idactividad', 'idclasetaller'),)


class Comportamiento(models.Model):
    idcomportamiento = models.AutoField(db_column='idComportamiento', primary_key=True)
    comentario = models.CharField(max_length=45)

    objects = ComportamientoManager()

    class Meta:
        db_table = 'comportamiento'


class Asistenciataller(models.Model):
    idasistenciataller = models.AutoField(db_column='idAsistenciaTaller', primary_key=True)
    estado = models.CharField(max_length=45)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idclasetaller = models.ForeignKey(Clasetaller, models.DO_NOTHING, db_column='idClaseTaller')
    idcomportamiento = models.ForeignKey(Comportamiento, models.DO_NOTHING, db_column='idComportamiento', blank=True, null=True)

    objects = AsistenciaTallerManager()

    class Meta:
        db_table = 'asistenciataller'


class Factorclase(models.Model):
    idclasetaller = models.OneToOneField(Clasetaller, models.DO_NOTHING, db_column='idClaseTaller', primary_key=True)
    idfactorglobal = models.ForeignKey('Factorglobal', models.DO_NOTHING, db_column='idFactorGlobal')

    objects = FactorClaseManager()

    class Meta:
        db_table = 'factorclase'
        unique_together = (('idclasetaller', 'idfactorglobal'),)


class Factorglobal(models.Model):
    idfactorglobal = models.AutoField(db_column='idFactorGlobal', primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = FactorGlobalManager()

    class Meta:
        db_table = 'factorglobal'


class Unidadobservacion(models.Model):
    idunidadobservacion = models.AutoField(db_column='idUnidadObservacion', primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = UnidadObservacionManager()

    class Meta:
        db_table = 'unidadobservacion'


class Variableuo(models.Model):
    idvariableuo = models.AutoField(db_column='idVariableUO', primary_key=True)
    nombre = models.CharField(max_length=45)
    idcomportamiento = models.ForeignKey(Comportamiento, models.DO_NOTHING, db_column='idComportamiento')
    idunidadobservacion = models.ForeignKey(Unidadobservacion, models.DO_NOTHING, db_column='idUnidadObservacion')

    objects = VariableUOManager()

    class Meta:
        db_table = 'variableuo'


class Valorvariableuo(models.Model):
    idvalorvariableuo = models.AutoField(db_column='idValorVariableUO', primary_key=True)
    valor = models.CharField(max_length=45)
    idvariableuo = models.ForeignKey(Variableuo, models.DO_NOTHING, db_column='idVariableUO')

    objects = ValorVariableUOManager()

    class Meta:
        db_table = 'valorvariableuo'
