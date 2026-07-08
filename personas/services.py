from core.exceptions import ServiceException, NotFoundException
from core.services import BaseService
from .models import (
    Persona, PersonaEp, Direccion, Tipoparentesco, Localidad, Municipio,
)


class PersonaService(BaseService):
    model = Persona


class PersonaEpService(BaseService):
    model = PersonaEp

    def listar(self):
        return self.model.objects.all().select_related('idpersona')


class DireccionService(BaseService):
    model = Direccion


class TipoParentescoService(BaseService):
    model = Tipoparentesco


class LocalidadService(BaseService):
    model = Localidad


class MunicipioService(BaseService):
    model = Municipio
