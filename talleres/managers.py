from django.db import IntegrityError, transaction

from core.managers import OrdenadoManager

CAMPOS_ORDEN_ENCUENTRO = ('fecha',)


class EncuentroManager(OrdenadoManager):
    """Manager de Encuentro con orden configurable."""

    def ordenar_por(self, campo, descendente=False, queryset=None):
        """Ordena por un campo permitido con desempate por PK."""
        base = self.listar_ordenado() if queryset is None else queryset
        prefijo = '-' if descendente else ''
        return base.order_by(f'{prefijo}{campo}', self.model._meta.pk.name)

    def ultimos_con_asistencias(self, limite=3):
        """Últimos encuentros con al menos una asistencia, por fecha DESC y PK ASC."""
        return self.filter(asistenciataller__isnull=False).distinct().order_by('-fecha', 'pk')[:limite]


class AsistenciaTallerManager(OrdenadoManager):
    """Manager para AsistenciaTaller con orden compuesto."""

    def listar_ordenado(self):
        return self.all().order_by('persona_ep', 'id_asistencia_taller')

    def estados_por_encuentro(self, encuentro):
        """Mapa persona_ep_id → estado persistido para el encuentro."""
        return dict(self.filter(encuentro=encuentro).values_list('persona_ep_id', 'estado'))

    def ausentes_por_encuentro(self, encuentro, estado):
        """IDs de PersonaEP con el estado indicado en el encuentro."""
        return self.filter(encuentro=encuentro, estado=estado).values_list('persona_ep_id', flat=True)

    def registrar_asistencia(self, persona_ep, encuentro, estado):
        """Crea la asistencia del par persona_ep + encuentro o actualiza su estado."""
        self.model.validar_estado(estado)
        # Operación ORM indivisible: la transacción local cubre el locking y el reintento por carrera.
        try:
            with transaction.atomic():
                asistencia = self.select_for_update().filter(persona_ep=persona_ep, encuentro=encuentro).first()
                if asistencia is None:
                    return self.create(persona_ep=persona_ep, encuentro=encuentro, estado=estado), True
                asistencia.estado = estado
                asistencia.save(update_fields=['estado'])
                return asistencia, False
        except IntegrityError:
            with transaction.atomic():
                asistencia = self.select_for_update().get(persona_ep=persona_ep, encuentro=encuentro)
                asistencia.estado = estado
                asistencia.save(update_fields=['estado'])
                return asistencia, False
