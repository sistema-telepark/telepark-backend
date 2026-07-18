from django.db import models

from core.managers import OrdenadoManager


class ObraSocialManager(OrdenadoManager):
    """Manager para Obrasocial con orden por PK."""


class OsManager(OrdenadoManager):
    """Manager para Os con orden por PK."""


class Obrasocial(models.Model):
    idobrasocial = models.AutoField(db_column='idObraSocial', primary_key=True)
    nombre = models.CharField(max_length=45)
    esestatal = models.IntegerField(db_column='esEstatal', blank=True, null=True)

    objects = ObraSocialManager()

    class Meta:
        db_table = 'obrasocial'


class Os(models.Model):
    idos = models.AutoField(db_column='idOS', primary_key=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idobrasocial = models.ForeignKey(Obrasocial, models.DO_NOTHING, db_column='idObraSocial')
    borrado = models.IntegerField(db_column='borrado')

    objects = OsManager()

    class Meta:
        db_table = 'os'
