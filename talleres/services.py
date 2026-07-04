from .models import (
    Taller, Clasetaller, Actividad, Actividadrealizada,
    Asistenciataller, Comportamiento, Factorclase, Factorglobal,
    Unidadobservacion, Variableuo, Valorvariableuo,
)


class ServiceException(Exception):
    pass


class NotFoundException(ServiceException):
    pass


class BaseService:
    model = None

    def listar(self):
        return self.model.objects.all()

    def obtener_por_id(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            raise NotFoundException(
                f"{self.model.__name__} with pk={pk} not found"
            )

    def crear(self, **datos):
        return self.model.objects.create(**datos)

    def actualizar(self, pk, **datos):
        obj = self.obtener_por_id(pk)
        for attr, value in datos.items():
            setattr(obj, attr, value)
        obj.save()
        return obj

    def eliminar(self, pk):
        obj = self.obtener_por_id(pk)
        obj.delete()


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
