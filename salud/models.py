from django.db import models

from core.managers import OrdenadoManager


class DiagnosticoManager(OrdenadoManager):
    """Manager para Diagnostico con orden por persona_ep + id_diagnostico."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_diagnostico')


class EvolucionManager(OrdenadoManager):
    """Manager para Evolucion con orden por persona_ep + id_evolucion."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_evolucion')


class IndicacionMedicamentoManager(OrdenadoManager):
    """Manager para IndicacionMedicamento con orden por persona_ep + id_indicacion."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_indicacion')


class Enfermedad(models.Model):
    id_enfermedad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = OrdenadoManager()

    class Meta:
        db_table = 'salud_enfermedad'


class Diagnostico(models.Model):
    id_diagnostico = models.AutoField(primary_key=True)
    fecha = models.DateField()
    persona_ep = models.ForeignKey('personas.PersonaEP', models.DO_NOTHING)
    enfermedad = models.ForeignKey(Enfermedad, models.DO_NOTHING)
    borrado = models.BooleanField(default=False)

    objects = DiagnosticoManager()

    class Meta:
        db_table = 'salud_diagnostico'


class Evolucion(models.Model):
    id_evolucion = models.AutoField(primary_key=True)
    escala_evolucion = models.IntegerField()
    fecha = models.DateField(blank=True, null=True)
    persona_ep = models.ForeignKey('personas.PersonaEP', models.DO_NOTHING)
    borrado = models.BooleanField(default=False)

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
    persona_ep = models.ForeignKey('personas.PersonaEP', models.DO_NOTHING)
    medicamento = models.ForeignKey(Medicamento, models.DO_NOTHING)
    borrado = models.BooleanField(default=False)

    objects = IndicacionMedicamentoManager()

    class Meta:
        db_table = 'salud_indicacion_medicamento'
