from core.exceptions import ServiceException, NotFoundException
from core.services import BaseService
from .models import (
    Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento,
)


class DiagnosticoService(BaseService):
    model = Diagnostico

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'iddiagnostico')

    def filtrar_por_persona(self, personaep_pk):
        return Diagnostico.objects.filter(idpersonaep=personaep_pk).select_related('idenfermedad')


class EvolucionService(BaseService):
    model = Evolucion

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'idevolucion')

    def filtrar_por_persona(self, personaep_pk):
        return Evolucion.objects.filter(idpersonaep=personaep_pk)


class EnfermedadService(BaseService):
    model = Enfermedad


class MedicamentoService(BaseService):
    model = Medicamento


class IndicacionService(BaseService):
    model = Indicacionmedicamento

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'idindicacion')

    def filtrar_por_persona(self, personaep_pk):
        return Indicacionmedicamento.objects.filter(idpersonaep=personaep_pk).select_related('idmedicamento')
