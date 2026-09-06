"""Módulo de carga del catálogo geográfico desde fixtures locales."""
import json
from pathlib import Path

from django.db import transaction

from .models import Departamento, Direccion, Localidad, Provincia

BATCH_SIZE = 1000  # bulk_create en batches

# Directorio y archivos de fixtures locales (fuente única de datos).
FIXTURES_DIR = Path(__file__).resolve().parent / 'fixtures' / 'georef'
FIXTURE_FILES = {
    'provincias': 'provincias.json',
    'departamentos': 'departamentos.json',
    'localidades': 'localidades.json',
}


class GeoRefError(Exception):
    """Error explícito de carga del catálogo geográfico."""


def _leer_fixture(clave):
    """Lee un fixture JSON y retorna la lista de ítems del envoltorio."""
    ruta = FIXTURES_DIR / FIXTURE_FILES[clave]
    try:
        with open(ruta, encoding='utf-8') as f:
            payload = json.load(f)
    except FileNotFoundError as e:
        raise GeoRefError(f'Fixture ausente: {ruta}') from e
    except json.JSONDecodeError as e:
        raise GeoRefError(f'Fixture JSON inválido ({ruta}): {e}') from e
    items = payload.get(clave)
    if not isinstance(items, list):
        raise GeoRefError(f'Fixture {ruta} no contiene la lista "{clave}"')
    return items


def _proximos_pks(modelo, cantidad):
    """Retorna el rango de PKs auto-incrementales a asignar explícitamente.

    ``bulk_create`` no puebla ``pk`` en las instancias con MySQL, así que los
    PKs se asignan de forma determinística antes del insert (seguro dentro de
    ``transaction.atomic()``, con las tablas vacías o recién borradas).
    """
    ultimo = modelo.objects.order_by('-pk').values_list('pk', flat=True).first()
    inicio = (ultimo or 0) + 1
    return range(inicio, inicio + cantidad)


def cargar_provincias():
    """Inserta provincias desde el fixture; retorna ``{id_fixture: pk}``."""
    items = _leer_fixture('provincias')
    provincias = [
        Provincia(pk=pk, nombre=item['nombre'])
        for pk, item in zip(_proximos_pks(Provincia, len(items)), items)
    ]
    Provincia.objects.bulk_create(provincias, batch_size=BATCH_SIZE)
    return {item['id']: p.pk for item, p in zip(items, provincias)}


def cargar_departamentos(mapa_provincias):
    """Inserta departamentos resolviendo ``idprovincia`` por mapa; retorna ``{id_fixture: pk}``."""
    items = _leer_fixture('departamentos')
    departamentos = [
        Departamento(
            pk=pk,
            nombre=item['nombre'],
            idprovincia_id=mapa_provincias.get(item['provincia']['id']),
        )
        for pk, item in zip(_proximos_pks(Departamento, len(items)), items)
    ]
    Departamento.objects.bulk_create(departamentos, batch_size=BATCH_SIZE)
    return {item['id']: d.pk for item, d in zip(items, departamentos)}


def _resolver_prioridad(categoria):
    """Prioridad de conservación de una localidad según su categoría (menor = mayor prioridad)."""
    return {
        'Entidad': 0,
        'Componente de localidad compuesta': 1,
        'Localidad simple': 2,
    }.get(categoria, 2)


def cargar_localidades(mapa_departamentos):
    """Inserta localidades resolviendo ``iddepartamento`` por mapa; retorna ``(persistidas, duplicados_eliminados)``.

    Deduplica por ``(iddepartamento, nombre)`` conservando el ítem de mayor
    prioridad (``_resolver_prioridad``); en empate, el de ``id`` más corto; en
    empate total, el primero en el orden del fixture.
    """
    items = _leer_fixture('localidades')
    ganadores = {}
    for item in items:
        clave = (mapa_departamentos.get(item['departamento']['id']), item['nombre'])
        actual = ganadores.get(clave)
        if actual is None:
            ganadores[clave] = item
            continue
        prioridad_actual = _resolver_prioridad(actual.get('categoria'))
        prioridad_nuevo = _resolver_prioridad(item.get('categoria'))
        if prioridad_nuevo < prioridad_actual or (
            prioridad_nuevo == prioridad_actual and len(item['id']) < len(actual['id'])
        ):
            ganadores[clave] = item
    ganadores = list(ganadores.values())
    localidades = [
        Localidad(
            pk=pk,
            nombre=item['nombre'],
            iddepartamento_id=mapa_departamentos.get(item['departamento']['id']),
            codigopostal=item.get('codigopostal'),
        )
        for pk, item in zip(_proximos_pks(Localidad, len(ganadores)), ganadores)
    ]
    Localidad.objects.bulk_create(localidades, batch_size=BATCH_SIZE)
    return len(localidades), len(items) - len(ganadores)


def _estado_catalogo():
    """Retorna ``'vacio'``, ``'poblado'`` o ``'mixto'`` según las 3 tablas."""
    estados = (
        Provincia.objects.exists(),
        Departamento.objects.exists(),
        Localidad.objects.exists(),
    )
    if all(estados):
        return 'poblado'
    if any(estados):
        return 'mixto'
    return 'vacio'


def _verificar_guard_integridad():
    """Aborta ``--force`` si existe una ``Direccion`` referenciando ``Localidad``."""
    if Direccion.objects.filter(idlocalidad__isnull=False).exists():
        raise GeoRefError(
            'No se puede forzar la recarga: existen direcciones referenciando '
            'localidades. Elimine o reasigne esas direcciones antes de usar --force.'
        )


def cargar_catalogo(force=False):
    """Carga el catálogo geográfico desde fixtures en una transacción atómica.

    Puerta de idempotencia todo-o-nada: con ``force=False`` carga solo si las 3
    tablas están vacías; si las 3 están pobladas retorna ``None`` (skip); si hay
    estado mixto levanta ``GeoRefError`` sin tocar nada. Con ``force=True``
    verifica el guard de integridad y recarga borrando en orden inverso de
    dependencia (localidades → departamentos → provincias).

    Retorna ``{'provincias': n, 'departamentos': n, 'localidades': n,
    'localidades_duplicadas_eliminadas': n}`` o ``None`` en el skip idempotente.
    """
    with transaction.atomic():
        if not force:
            estado = _estado_catalogo()
            if estado == 'poblado':
                return None
            if estado == 'mixto':
                raise GeoRefError(
                    'Estado inconsistente del catálogo: algunas tablas están '
                    'pobladas y otras vacías. No se modifica la BD.'
                )
        else:
            _verificar_guard_integridad()
            Localidad.objects.all().delete()
            Departamento.objects.all().delete()
            Provincia.objects.all().delete()

        mapa_provincias = cargar_provincias()
        mapa_departamentos = cargar_departamentos(mapa_provincias)
        n_localidades, n_duplicadas = cargar_localidades(mapa_departamentos)

    return {
        'provincias': len(mapa_provincias),
        'departamentos': len(mapa_departamentos),
        'localidades': n_localidades,
        'localidades_duplicadas_eliminadas': n_duplicadas,
    }