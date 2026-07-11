from core.services import BaseService
from .models import (
    Taller, Clasetaller, Actividad, Actividadrealizada,
    Asistenciataller, Comportamiento, Factorclase, Factorglobal,
    Unidadobservacion, Variableuo, Valorvariableuo,
)


class TallerService(BaseService):
    model = Taller


class ClaseTallerService(BaseService):
    model = Clasetaller


class ActividadService(BaseService):
    model = Actividad


class ActividadRealizadaService(BaseService):
    model = Actividadrealizada


class AsistenciaTallerService(BaseService):
    model = Asistenciataller

    def listar(self):
        return self.model.objects.all().order_by('idpersonaep', 'idasistenciataller')


class ComportamientoService(BaseService):
    model = Comportamiento


class FactorClaseService(BaseService):
    model = Factorclase


class FactorGlobalService(BaseService):
    model = Factorglobal


class UnidadObservacionService(BaseService):
    model = Unidadobservacion


class VariableUOService(BaseService):
    model = Variableuo


class ValorVariableUOService(BaseService):
    model = Valorvariableuo
