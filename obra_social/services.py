from core.services import BaseService
from .models import Obrasocial, Os


class ObraSocialService(BaseService):
    model = Obrasocial


class OsService(BaseService):
    model = Os


