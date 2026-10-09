from django.db import models

from core.managers import OrdenadoManager


class EventoManager(OrdenadoManager):
    """Manager para Evento con select_related + orden compuesto."""

    def listar_ordenado(self):
        return self.all().select_related('tipo_evento').order_by('persona_ep', 'id_evento')


class TipoEvento(models.Model):
    id_tipo_evento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    desactiva_taller = models.BooleanField(default=False)
    borrado = models.BooleanField(default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'eventos_tipo_evento'


class Evento(models.Model):
    id_evento = models.AutoField(primary_key=True)
    fecha_desde = models.DateField(blank=True, null=True)
    fecha_hasta = models.DateField(blank=True, null=True)
    motivo = models.CharField(max_length=256, blank=True, null=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.DO_NOTHING)
    tipo_evento = models.ForeignKey(TipoEvento, models.DO_NOTHING)
    borrado = models.BooleanField(default=False)

    objects = EventoManager()

    class Meta:
        db_table = 'eventos_evento'
