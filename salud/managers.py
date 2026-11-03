from core.managers import OrdenadoManager


class DiagnosticoManager(OrdenadoManager):
    """Manager para Diagnostico con orden por persona_ep + id_diagnostico."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_diagnostico')


class EvolucionManager(OrdenadoManager):
    """Manager para Evolucion con orden por persona_ep + id_evolucion."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_evolucion')


class IndicacionMedicamentoManager(OrdenadoManager):
    """Manager para IndicacionMedicamento con orden por persona_ep + id_indicacion."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_indicacion')
