from django.db import models

from core.managers import OrdenadoManager


class EventoManager(OrdenadoManager):
    """Manager para Evento con select_related + orden compuesto."""

    def listar_ordenado(self):
        return self.all().select_related('tipo_evento').order_by('persona_ep', 'id_evento')

    def justificaciones_en_lote(self, personas_ids, fechas):
        """Pares (persona_ep_id, fecha) cubiertos por algún evento, resueltos en una sola consulta."""
        personas = list(personas_ids)
        objetivo = [fecha for fecha in fechas if fecha is not None]
        if not personas or not objetivo:
            return set()
        fecha_min = min(objetivo)
        fecha_max = max(objetivo)
        eventos = (
            self.filter(persona_ep_id__in=personas)
            .filter(models.Q(fecha_desde__isnull=True) | models.Q(fecha_desde__lte=fecha_max))
            .filter(models.Q(fecha_hasta__isnull=True) | models.Q(fecha_hasta__gte=fecha_min))
            .exclude(fecha_desde__isnull=True, fecha_hasta__isnull=True)
            .values_list('persona_ep_id', 'fecha_desde', 'fecha_hasta')
        )
        justificadas = set()
        for persona_ep_id, desde, hasta in eventos:
            for fecha in objetivo:
                if (desde is None or desde <= fecha) and (hasta is None or hasta >= fecha):
                    justificadas.add((persona_ep_id, fecha))
        return justificadas
