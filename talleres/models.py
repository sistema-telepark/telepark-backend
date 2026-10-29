from django.apps import apps
from django.db import IntegrityError, models, transaction

from core.exceptions import ConflictError, ValidationError
from core.managers import OrdenadoManager

ESTADOS_ASISTENCIA = (
    ('Presente', 'Presente'),
    ('Ausente', 'Ausente'),
)
ESTADO_ASISTENCIA_DEFAULT = 'Ausente'


class AsistenciaTallerManager(OrdenadoManager):
    """Manager para AsistenciaTaller con orden compuesto."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_asistencia_taller')

    def listar_roster(self, encuentro):
        """Filas del roster del encuentro, una por PersonaEP activa ordenada por PK."""
        PersonaEP = apps.get_model('personas', 'PersonaEP')
        estados = dict(self.filter(encuentro=encuentro).values_list('persona_ep_id', 'estado'))
        personas = PersonaEP.objects.filtrar_por_activo(True).values_list('pk', flat=True)
        return [
            {'persona_ep': persona_ep, 'estado': estados.get(persona_ep, ESTADO_ASISTENCIA_DEFAULT)}
            for persona_ep in personas
        ]

    def registrar_asistencia(self, persona_ep, encuentro, estado):
        """Crea la asistencia del par persona_ep + encuentro o actualiza su estado."""
        AsistenciaTaller.validar_estado(estado)
        try:
            with transaction.atomic():
                asistencia = self.select_for_update().filter(persona_ep=persona_ep, encuentro=encuentro).first()
                if asistencia is None:
                    return self.create(persona_ep=persona_ep, encuentro=encuentro, estado=estado), True
                asistencia.estado = estado
                asistencia.save(update_fields=['estado'])
                return asistencia, False
        except IntegrityError:
            with transaction.atomic():
                asistencia = self.select_for_update().get(persona_ep=persona_ep, encuentro=encuentro)
                asistencia.estado = estado
                asistencia.save(update_fields=['estado'])
                return asistencia, False


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
        constraints = [
            models.UniqueConstraint(fields=('encuentro', 'actividad'), name='unique_encuentro_actividad_pair'),
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
    encuentro_actividad = models.ForeignKey(EncuentroActividad, models.CASCADE, blank=True, null=True)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'talleres_valor_variable_uo'
