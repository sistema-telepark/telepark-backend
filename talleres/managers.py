from core.managers import OrdenadoManager

CAMPOS_ORDEN_ENCUENTRO = ('fecha',)


class EncuentroManager(OrdenadoManager):
    """Manager de Encuentro con orden configurable."""

    def ordenar_por(self, campo, descendente=False, queryset=None):
        """Ordena por un campo permitido con desempate por PK."""
        base = self.listar_ordenado() if queryset is None else queryset
        prefijo = '-' if descendente else ''
        return base.order_by(f'{prefijo}{campo}', self.model._meta.pk.name)
