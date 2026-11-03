from django.db import models

from core.managers import OrdenadoManager

from .managers import DiagnosticoManager, EvolucionManager, IndicacionMedicamentoManager


class Enfermedad(models.Model):
    id_enfermedad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'salud_enfermedad'


class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True)
    fecha = models.DateField()
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT)
    enfermedad = models.ForeignKey(Enfermedad, models.PROTECT)

    objects = DiagnosticoManager()

    class Meta:
        db_table = 'salud_diagnostico'


class Evolucion(models.Model):
    id_evolucion = models.AutoField(primary_key=True)
    escala_evolucion = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT)

    objects = EvolucionManager()

    class Meta:
        db_table = 'salud_evolucion'


class Medicamento(models.Model):
    id_medicamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    es_antiparkinsoniano = models.BooleanField(default=False)
    es_levodopa = models.BooleanField(default=False)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'salud_medicamento'


class IndicacionMedicamento(models.Model):
    id_indicacion = models.AutoField(primary_key=True)
    cantidad_miligramos = models.IntegerField(blank=True, null=True)
    esta_vigente = models.BooleanField(default=False)
    fecha_prescripcion = models.DateField(blank=True, null=True)
    hora_de_toma = models.TimeField(blank=True, null=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.PROTECT)
    medicamento = models.ForeignKey(Medicamento, models.PROTECT)

    objects = IndicacionMedicamentoManager()

    class Meta:
        db_table = 'salud_indicacion_medicamento'
