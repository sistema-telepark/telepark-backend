from django.db import models

from core.managers import OrdenadoManager


class EventoManager(OrdenadoManager):
    """Manager para Evento con select_related + orden compuesto."""

    def listar_ordenado(self):
        return self.all().select_related('idtipoevento').order_by('idpersonaep', 'idevento')


class Tipoevento(models.Model):
    idtipoevento = models.AutoField(db_column='idTipoEvento', primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    desactivataller = models.BooleanField(db_column='desactivaTaller', default=False)
    borrado = models.BooleanField(db_column='borrado', default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'tipoevento'


class Evento(models.Model):
    idevento = models.AutoField(db_column='idEvento', primary_key=True)
    fechadesde = models.DateField(db_column='fechaDesde', blank=True, null=True)
    fechahasta = models.DateField(db_column='fechaHasta', blank=True, null=True)
    motivo = models.CharField(max_length=256, blank=True, null=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idtipoevento = models.ForeignKey(Tipoevento, models.DO_NOTHING, db_column='idTipoEvento')
    borrado = models.BooleanField(db_column='borrado', default=False)

    objects = EventoManager()

    class Meta:
        db_table = 'evento'
