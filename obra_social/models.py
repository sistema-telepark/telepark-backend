from django.db import models


class Obrasocial(models.Model):
    idobrasocial = models.AutoField(db_column='idObraSocial', primary_key=True)
    nombre = models.CharField(max_length=45)
    esestatal = models.IntegerField(db_column='esEstatal', blank=True, null=True)

    class Meta:
        db_table = 'obrasocial'


class Os(models.Model):
    idos = models.AutoField(db_column='idOS', primary_key=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idobrasocial = models.ForeignKey(Obrasocial, models.DO_NOTHING, db_column='idObraSocial')
    borrado = models.IntegerField(db_column='borrado')

    class Meta:
        db_table = 'os'
