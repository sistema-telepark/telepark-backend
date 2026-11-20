from django.db import models

from core.exceptions import ConflictError, ValidationError
from core.managers import OrdenadoManager

from .managers import AsistenciaTallerManager, EncuentroManager

ESTADOS_ASISTENCIA = (
    ('Presente', 'Presente'),
    ('Ausente', 'Ausente'),
)
ESTADO_ASISTENCIA_DEFAULT = 'Ausente'


class Taller(models.Model):
    id_taller = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.encuentros_talleres.exists() or self.actividad_set.exists():
            raise ConflictError('No se puede eliminar un taller con encuentros o actividades asociados')

    class Meta:
        db_table = 'talleres_taller'


class Encuentro(models.Model):
    id_encuentro = models.AutoField(primary_key=True)
    fecha = models.DateField()
    virtual = models.BooleanField(default=False)

    objects = EncuentroManager()

    class Meta:
        db_table = 'talleres_encuentro'


class EncuentroTaller(models.Model):
    id_encuentro_taller = models.AutoField(primary_key=True)
    encuentro = models.ForeignKey(Encuentro, models.CASCADE, related_name='talleres')
    taller = models.ForeignKey(Taller, models.PROTECT, related_name='encuentros_talleres')

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_encuentro_taller'
        constraints = [
            models.UniqueConstraint(fields=('encuentro', 'taller'), name='unique_encuentro_taller_pair'),
        ]


class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    taller = models.ForeignKey(Taller, models.PROTECT)

    objects = OrdenadoManager()

    def validar_borrado(self):
        if self.encuentrotalleractividad_set.exists():
            raise ConflictError('No se puede eliminar una actividad con registros de actividades realizadas')

    class Meta:
        db_table = 'talleres_actividad'


class EncuentroTallerActividad(models.Model):
    id_encuentro_taller_actividad = models.AutoField(primary_key=True)
    encuentro_taller = models.ForeignKey(EncuentroTaller, models.CASCADE, related_name='actividades_realizadas')
    actividad = models.ForeignKey(Actividad, models.PROTECT)

    objects = OrdenadoManager()

    @staticmethod
    def validar_actividad(actividad, encuentro_taller):
        """Rechaza una actividad que no pertenece al taller del encuentro-taller."""
        if actividad.taller_id != encuentro_taller.taller_id:
            raise ValidationError('La actividad debe pertenecer al mismo taller que el encuentro-taller')

    def validar_borrado(self):
        if self.valorvariableuo_set.exists():
            raise ConflictError('No se puede eliminar una actividad realizada con valores de variable UO asociados')

    class Meta:
        db_table = 'talleres_encuentro_taller_actividad'
        constraints = [
            models.UniqueConstraint(
                fields=('encuentro_taller', 'actividad'), name='unique_encuentro_taller_actividad_pair'
            ),
        ]


class AsistenciaTaller(models.Model):
    id_asistencia_taller = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=45, choices=ESTADOS_ASISTENCIA)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT)
    encuentro = models.ForeignKey(Encuentro, models.PROTECT)

    objects = AsistenciaTallerManager()

    @staticmethod
    def validar_estado(estado):
        if estado not in dict(ESTADOS_ASISTENCIA):
            raise ValidationError(f'Estado inválido: "{estado}". Valores permitidos: Presente, Ausente.')

    def validar_disponibilidad(self, persona_ep, encuentro):
        """Rechaza el par persona_ep + encuentro si otra fila ya lo ocupa."""
        if AsistenciaTaller.objects.filter(persona_ep=persona_ep, encuentro=encuentro).exclude(pk=self.pk).exists():
            raise ConflictError('Ya existe una asistencia para esa persona en el encuentro indicado')

    class Meta:
        db_table = 'talleres_asistencia_taller'
        constraints = [
            models.UniqueConstraint(
                fields=('persona_ep', 'encuentro'), name='unique_asistencia_taller_persona_ep_encuentro'
            ),
        ]


class EncuentroFactorGlobal(models.Model):
    id_encuentro_factor_global = models.AutoField(primary_key=True)
    encuentro = models.ForeignKey(Encuentro, models.CASCADE)
    factor_global = models.ForeignKey('FactorGlobal', models.PROTECT)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_encuentro_factor_global'
        constraints = [
            models.UniqueConstraint(fields=('encuentro', 'factor_global'), name='unique_encuentro_factor_global_pair'),
        ]


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
    encuentro_taller_actividad = models.ForeignKey(EncuentroTallerActividad, models.PROTECT, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_valor_variable_uo'
