from core.services import BaseService
from .models import (
    Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento,
)


class DiagnosticoService(BaseService):
    model = Diagnostico

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'iddiagnostico')

class EvolucionService(BaseService):
    model = Evolucion

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'idevolucion')

class EnfermedadService(BaseService):
    model = Enfermedad


class MedicamentoService(BaseService):
    model = Medicamento


class IndicacionService(BaseService):
    model = Indicacionmedicamento

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'idindicacion')


