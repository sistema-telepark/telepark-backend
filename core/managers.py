from django.db import models


class OrdenadoManager(models.Manager):
    """Manager base que provee listar_ordenado() por PK y filtrar_por_persona().

    Es la alternativa Django nativa a BaseService — reemplaza el CRUD genérico
    con métodos de Manager, que es el lugar que Django prescribe para lógica
    de consultas (table-level).
    """

    def listar_ordenado(self):
        """Retorna todos los registros ordenados por PK (orden determinístico)."""
        return self.all().order_by(self.model._meta.pk.name)

    def filtrar_por_persona(self, personaep_pk, select_related_fields=None):
        """Filtra registros por FK a PersonaEp, con select_related opcional.

        Args:
            personaep_pk: PK de la persona (paciente) a filtrar
            select_related_fields: lista de campos para select_related (ej: ['idtipoevento'])
        """
        qs = self.filter(idpersonaep=personaep_pk)
        if select_related_fields:
            qs = qs.select_related(*select_related_fields)
        return qs
