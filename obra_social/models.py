from django.db import models

from core.managers import OrdenadoManager


class Obrasocial(models.Model):
    idobrasocial = models.AutoField(db_column='idObraSocial', primary_key=True)
    nombre = models.CharField(max_length=45)
    esestatal = models.BooleanField(db_column='esEstatal', default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'obrasocial'


class Os(models.Model):
    idos = models.AutoField(db_column='idOS', primary_key=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idobrasocial = models.ForeignKey(Obrasocial, models.DO_NOTHING, db_column='idObraSocial')
    borrado = models.BooleanField(db_column='borrado', default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'os'
