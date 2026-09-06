from core.managers import OrdenadoManager


class NombreOrderedManager(OrdenadoManager):
    """Manager de consultas con orden alfabético por nombre."""

    def listar_ordenado(self):
        return self.all().order_by('nombre')