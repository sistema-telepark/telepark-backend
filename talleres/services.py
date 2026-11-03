from eventos.models import Evento
from personas.models import PersonaEP

from .models import ESTADO_ASISTENCIA_DEFAULT, AsistenciaTaller, Encuentro

CANTIDAD_ENCUENTROS_FALTAS = 3


def listar_roster(encuentro):
    """Roster del encuentro: una fila por PersonaEP activa con estado y justificación."""
    estados = AsistenciaTaller.objects.estados_por_encuentro(encuentro)
    personas = list(PersonaEP.objects.filtrar_por_activo(True).values_list('pk', flat=True))
    justificadas = Evento.objects.justificaciones_en_lote(personas, [encuentro.fecha])
    filas = []
    for persona_ep in personas:
        estado = estados.get(persona_ep, ESTADO_ASISTENCIA_DEFAULT)
        justificada = estado == ESTADO_ASISTENCIA_DEFAULT and (persona_ep, encuentro.fecha) in justificadas
        filas.append({'persona_ep': persona_ep, 'estado': estado, 'justificada': justificada})
    return filas


def listar_faltas_consecutivas():
    """PersonaEP activas con ausencia injustificada en los tres encuentros de la ventana."""
    encuentros = list(Encuentro.objects.ultimos_con_asistencias(CANTIDAD_ENCUENTROS_FALTAS))
    if len(encuentros) < CANTIDAD_ENCUENTROS_FALTAS:
        return []
    candidatos = set(PersonaEP.objects.filtrar_por_activo(True).values_list('pk', flat=True))
    for encuentro in encuentros:
        candidatos &= set(AsistenciaTaller.objects.ausentes_por_encuentro(encuentro, ESTADO_ASISTENCIA_DEFAULT))
    fechas = [encuentro.fecha for encuentro in encuentros]
    justificadas = Evento.objects.justificaciones_en_lote(candidatos, fechas)
    elegibles = [
        persona_ep
        for persona_ep in sorted(candidatos)
        if not any((persona_ep, fecha) in justificadas for fecha in fechas)
    ]
    return [
        {
            'persona_ep': persona_ep,
            'encuentros': [
                {
                    'encuentro': encuentro.pk,
                    'fecha': encuentro.fecha,
                    'estado': ESTADO_ASISTENCIA_DEFAULT,
                    'justificada': False,
                }
                for encuentro in encuentros
            ],
        }
        for persona_ep in elegibles
    ]
