from core.exceptions import ServiceException, NotFoundException
from core.services import BaseService
from .models import Evento, Tipoevento


class EventoService(BaseService):
    model = Evento

    def listar(self):
        return self.model.objects.all().select_related('idtipoevento')


class TipoEventoService(BaseService):
    model = Tipoevento
