from django.db import models

from core.managers import OrdenadoManager


class DiagnosticoManager(OrdenadoManager):
    """Manager para Diagnostico con orden por idpersonaep + iddiagnostico."""

    def listar_ordenado(self):
        return self.all().order_by('idpersonaep', 'iddiagnostico')


class EvolucionManager(OrdenadoManager):
    """Manager para Evolucion con orden por idpersonaep + idevolucion."""

    def listar_ordenado(self):
        return self.all().order_by('idpersonaep', 'idevolucion')


class EnfermedadManager(OrdenadoManager):
    """Manager para Enfermedad — solo orden por PK."""


class MedicamentoManager(OrdenadoManager):
    """Manager para Medicamento — solo orden por PK."""


class IndicacionManager(OrdenadoManager):
    """Manager para Indicacionmedicamento con orden por idpersonaep + idindicacion."""

    def listar_ordenado(self):
        return self.all().order_by('idpersonaep', 'idindicacion')


class Enfermedad(models.Model):
    idenfermedad = models.AutoField(db_column='idEnfermedad', primary_key=True)
    nombre = models.CharField(max_length=45)

    objects = EnfermedadManager()

    class Meta:
        db_table = 'enfermedad'


class Diagnostico(models.Model):
    iddiagnostico = models.AutoField(db_column='idDiagnostico', primary_key=True)
    fecha = models.DateField()
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idenfermedad = models.ForeignKey(Enfermedad, models.DO_NOTHING, db_column='idEnfermedad')
    borrado = models.IntegerField(db_column='borrado')

    objects = DiagnosticoManager()

    class Meta:
        db_table = 'diagnostico'


class Evolucion(models.Model):
    idevolucion = models.AutoField(db_column='idEvolucion', primary_key=True)
    escalaevolucion = models.IntegerField(db_column='escalaEvolucion')
    fecha = models.DateField(blank=True, null=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    borrado = models.IntegerField(db_column='borrado')

    objects = EvolucionManager()

    class Meta:
        db_table = 'evolucion'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(db_column='idMedicamento', primary_key=True)
    nombre = models.CharField(max_length=45)
    esantiparkinsoniano = models.IntegerField(db_column='esAntiparkinsoniano', blank=True, null=True)
    eslevodopa = models.IntegerField(db_column='esLevodopa', blank=True, null=True)

    objects = MedicamentoManager()

    class Meta:
        db_table = 'medicamento'


class Indicacionmedicamento(models.Model):
    idindicacion = models.AutoField(db_column='idIndicacion', primary_key=True)
    cantidadmiligramos = models.IntegerField(db_column='cantidadMiligramos', blank=True, null=True)
    estavigente = models.IntegerField(db_column='estaVigente', blank=True, null=True)
    fechaprescripcion = models.DateField(db_column='fechaPrescripcion', blank=True, null=True)
    horadetoma = models.TimeField(db_column='horaDeToma', blank=True, null=True)
    idpersonaep = models.ForeignKey('personas.PersonaEp', models.DO_NOTHING, db_column='idPersonaEP')
    idmedicamento = models.ForeignKey(Medicamento, models.DO_NOTHING, db_column='idMedicamento')
    borrado = models.IntegerField(db_column='borrado')

    objects = IndicacionManager()

    class Meta:
        db_table = 'indicacionmedicamento'
