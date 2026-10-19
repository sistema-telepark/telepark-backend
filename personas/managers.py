from core.managers import OrdenadoManager


class NombreOrderedManager(OrdenadoManager):
    """Manager de consultas con orden alfabético por nombre."""

    def listar_ordenado(self):
        return self.all().order_by('nombre')


class PersonaManager(OrdenadoManager):
    """Manager de Persona/PersonaEP con filtrado por estado activo."""

    def filtrar_por_activo(self, activo):
        return self.listar_ordenado().filter(activo=activo)
