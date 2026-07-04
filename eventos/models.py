from django.db import models


class Tipoevento(models.Model):
    idtipoevento = models.AutoField(db_column='idTipoEvento', primary_key=True)
    nombre = models.CharField(max_length=45, blank=True, null=True)
    desactivataller = models.IntegerField(db_column='desactivaTaller', blank=True, null=True)
    borrado = models.IntegerField(db_column='borrado')

    class Meta:
        db_table = 'tipoevento'


class Evento(models.Model):
    idevento = models.AutoField(db_column='idEvento', primary_key=True)
    fechadesde = models.DateField(db_column='fechaDesde', blank=True, null=True)
    fechahasta = models.DateField(db_column='fechaHasta', blank=True, null=True)
    motivo = models.CharField(max_length=256, blank=True, null=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idtipoevento = models.ForeignKey(Tipoevento, models.DO_NOTHING, db_column='idTipoEvento')
    borrado = models.IntegerField(db_column='borrado')

    class Meta:
        db_table = 'evento'
