from core.services import BaseService
from .models import Evento, Tipoevento


class EventoService(BaseService):
    model = Evento

    def listar(self):
        return self.model.objects.all().select_related('idtipoevento').order_by('idpersonaep', 'idevento')


class TipoEventoService(BaseService):
    model = Tipoevento
