from django.db import models

from core.managers import OrdenadoManager


class ObraSocial(models.Model):
    id_obra_social = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    es_estatal = models.BooleanField(default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'obra_social_obra_social'


class Cobertura(models.Model):
    id_cobertura = models.AutoField(primary_key=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.DO_NOTHING)
    obra_social = models.ForeignKey(ObraSocial, models.DO_NOTHING)
    borrado = models.BooleanField(default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'obra_social_cobertura'
