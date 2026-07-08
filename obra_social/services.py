from core.exceptions import ServiceException, NotFoundException
from core.services import BaseService
from .models import Obrasocial, Os


class ObraSocialService(BaseService):
    model = Obrasocial


class OsService(BaseService):
    model = Os

    def filtrar_por_persona(self, personaep_pk):
        return Os.objects.filter(idpersonaep=personaep_pk).select_related('idobrasocial')
