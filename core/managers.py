from django.db import models


class OrdenadoManager(models.Manager):
    """Manager base de lógica de consultas con orden determinístico por PK."""

    def listar_ordenado(self):
        """Retorna todos los registros ordenados por PK (orden determinístico)."""
        return self.all().order_by(self.model._meta.pk.name)

    def filtrar_por_persona_ep(self, personaep_pk, select_related_fields=None):
        """Filtra registros por FK a PersonaEp, con select_related opcional.

        Args:
            personaep_pk: PK de la persona (paciente) a filtrar
            select_related_fields: lista de campos para select_related (ej: ['idtipoevento'])
        """
        qs = self.filter(idpersonaep=personaep_pk)
        if select_related_fields:
            qs = qs.select_related(*select_related_fields)
        return qs
