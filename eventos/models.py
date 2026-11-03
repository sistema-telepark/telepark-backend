from django.db import models

from core.managers import OrdenadoManager


class EventoManager(OrdenadoManager):
    """Manager para Evento con select_related + orden compuesto."""

    def listar_ordenado(self):
        return self.all().select_related('tipo_evento').order_by('persona_ep', 'id_evento')

    def justifica_fecha(self, persona_ep, fecha):
        """Indica si algún evento de la persona cubre `fecha` (puntas nulas abiertas)."""
        if fecha is None:
            return False
        return (
            self.filter(persona_ep=persona_ep)
            .filter(models.Q(fecha_desde__isnull=True) | models.Q(fecha_desde__lte=fecha))
            .filter(models.Q(fecha_hasta__isnull=True) | models.Q(fecha_hasta__gte=fecha))
            .exclude(fecha_desde__isnull=True, fecha_hasta__isnull=True)
            .exists()
        )


class TipoEvento(models.Model):
    id_tipo_evento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    desactiva_taller = models.BooleanField(default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'eventos_tipo_evento'


class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    motivo = models.CharField(max_length=256, blank=True, null=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT)
    tipo_evento = models.ForeignKey(TipoEvento, models.PROTECT)

    objects = EventoManager()

    class Meta:
        db_table = 'eventos_evento'
