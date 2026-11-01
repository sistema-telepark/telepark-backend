from core.managers import OrdenadoManager

CAMPOS_ORDEN_PERSONA = ('apellido', 'nombre')


class NombreOrderedManager(OrdenadoManager):
    """Manager de consultas con orden alfabético por nombre."""

    def listar_ordenado(self):
        return self.all().order_by('nombre')


class PersonaManager(OrdenadoManager):
    """Manager de Persona/PersonaEP con filtrado por estado activo y orden configurable."""

    def filtrar_por_activo(self, activo):
        return self.listar_ordenado().filter(activo=activo)

    def ordenar_por(self, campo, descendente=False, queryset=None):
        """Ordena por un campo permitido con desempate por PK."""
        base = self.listar_ordenado() if queryset is None else queryset
        prefijo = '-' if descendente else ''
        return base.order_by(f'{prefijo}{campo}', self.model._meta.pk.name)
