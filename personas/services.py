from django.db import transaction

from core.exceptions import ValidationError

from .models import PersonaEP, Vinculo


def reordenar_vinculos(persona_ep_pk, ids_vinculo):
    """Asigna posiciones 1..N a la secuencia completa de vínculos del paciente."""
    with transaction.atomic():
        persona_ep = PersonaEP.objects.select_for_update().get(pk=persona_ep_pk)
        vinculos = list(Vinculo.objects.select_for_update().filter(persona_ep=persona_ep))
        ids_paciente = {vinculo.pk for vinculo in vinculos}
        if len(ids_vinculo) != len(ids_paciente) or set(ids_vinculo) != ids_paciente:
            raise ValidationError(
                {'vinculos': [f'La secuencia debe incluir exactamente los {len(ids_paciente)} vínculos del paciente.']}
            )
        Vinculo.objects.filter(pk__in=ids_paciente).update(orden_llamada=None)
        for posicion, id_vinculo in enumerate(ids_vinculo, start=1):
            Vinculo.objects.filter(pk=id_vinculo).update(orden_llamada=posicion)
