from core.exceptions import ServiceException, NotFoundException


class BaseService:
    model = None

    def listar(self):
        return self.model.objects.all().order_by(self.model._meta.pk.name)

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
