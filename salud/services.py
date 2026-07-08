from .models import (
    Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento,
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
