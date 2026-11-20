from django.db.models import F

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


class VinculoManager(OrdenadoManager):
    """Manager de Vinculo con la secuencia de contacto efectiva."""

    def listar_por_orden_contacto(self, persona_ep_pk=None):
        """Vínculos de contactos activos ordenados por posición (NULL al final)."""
        qs = self.filter(persona__activo=True)
        if persona_ep_pk is not None:
            qs = qs.filter(persona_ep=persona_ep_pk)
        return qs.order_by(F('orden_contacto').asc(nulls_last=True), self.model._meta.pk.name)
