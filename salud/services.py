from core.exceptions import ServiceException, NotFoundException
from core.services import BaseService
from .models import (
    Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento,
)


class DiagnosticoService(BaseService):
    model = Diagnostico

    def filtrar_por_persona(self, personaep_pk):
        return Diagnostico.objects.filter(idpersonaep=personaep_pk).select_related('idenfermedad')


class EvolucionService(BaseService):
    model = Evolucion

    def filtrar_por_persona(self, personaep_pk):
        return Evolucion.objects.filter(idpersonaep=personaep_pk)


class EnfermedadService(BaseService):
    model = Enfermedad


class MedicamentoService(BaseService):
    model = Medicamento


class IndicacionService(BaseService):
    model = Indicacionmedicamento

    def filtrar_por_persona(self, personaep_pk):
        return Indicacionmedicamento.objects.filter(idpersonaep=personaep_pk).select_related('idmedicamento')
