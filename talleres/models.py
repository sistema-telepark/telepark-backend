from django.db import models

from core.exceptions import ConflictError
from core.managers import OrdenadoManager


class AsistenciaTallerManager(OrdenadoManager):
    """Manager para AsistenciaTaller con orden compuesto."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_asistencia_taller')


class Taller(models.Model):
    id_taller = models.AutoField(primary_key=True)
    tipo_taller = models.CharField(max_length=45)

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.encuentro_set.exists() or self.actividad_set.exists():
            raise ConflictError('No se puede eliminar un taller con encuentros o actividades asociados')

    class Meta:
        db_table = 'talleres_taller'


class Encuentro(models.Model):
    id_encuentro = models.AutoField(primary_key=True)
    fecha = models.DateField()
    virtual = models.BooleanField(default=False)
    taller = models.ForeignKey(Taller, models.PROTECT)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_encuentro'


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    taller = models.ForeignKey(Taller, models.PROTECT)

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.encuentroactividad_set.exists():
            raise ConflictError('No se puede eliminar una actividad con registros de actividades realizadas')

    class Meta:
        db_table = 'talleres_actividad'


class EncuentroActividad(models.Model):
    id_encuentro_actividad = models.AutoField(primary_key=True)
    actividad = models.ForeignKey(Actividad, models.PROTECT)
    encuentro = models.ForeignKey(Encuentro, models.CASCADE)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_encuentro_actividad'
        unique_together = (('actividad', 'encuentro'),)


class AsistenciaTaller(models.Model):
    id_asistencia_taller = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=45)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT, blank=True, null=True)
    encuentro = models.ForeignKey(Encuentro, models.SET_NULL, blank=True, null=True)

    objects = AsistenciaTallerManager()

    class Meta:
        db_table = 'talleres_asistencia_taller'


class EncuentroFactorGlobal(models.Model):
    id_encuentro_factor_global = models.AutoField(primary_key=True)
    encuentro = models.ForeignKey(Encuentro, models.CASCADE)
    factor_global = models.ForeignKey('FactorGlobal', models.PROTECT)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_encuentro_factor_global'
        unique_together = (('encuentro', 'factor_global'),)


class FactorGlobal(models.Model):
    id_factor_global = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_factor_global'


class UnidadObservacion(models.Model):
    id_unidad_observacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_unidad_observacion'


class VariableUO(models.Model):
    id_variable_uo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    unidad_observacion = models.ForeignKey(UnidadObservacion, models.PROTECT)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_variable_uo'


class ValorVariableUO(models.Model):
    id_valor_variable_uo = models.AutoField(primary_key=True)
    valor = models.CharField(max_length=45)
    variable_uo = models.ForeignKey(VariableUO, models.PROTECT)
    asistencia_taller = models.ForeignKey(AsistenciaTaller, models.CASCADE, blank=True, null=True)
    encuentro_actividad = models.ForeignKey(EncuentroActividad, models.CASCADE, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_valor_variable_uo'
