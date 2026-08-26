"""Módulo de carga del catálogo geográfico GeoRef (E8).

Funciones standalone (sin clases, sin service layer — ADR-001), siguiendo el
patrón de ``autenticacion/helpers.py``. Solo ``urllib`` de la stdlib para HTTP
(REQ-E8-002, SEC-E8-005): PROHIBIDO agregar dependencias nuevas.

Estrategia en dos fases (decisión HITL 2026-08-19):
1. offline — ``cargar_georef --solo-descargar`` genera fixtures JSON commiteados.
2. despliegue — ``cargar_georef`` carga desde fixtures (fuente primaria) con
   fallback a la API GeoRef.

Los departamentos se ignoran (decisión del roadmap). Los IDs originales de
GeoRef se preservan en ``id_georef`` (Opción 1, decisión HITL 2026-08-19).
El catálogo de localidades se descarga desde ``/localidades-censales`` (INDEC)
como fuente única (E11, decisión HITL 2026-08-26); la clave de payload es
``localidades_censales`` (guión bajo), distinta de la ruta del endpoint.
"""
import json
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from django.conf import settings

from .models import Localidad, Municipio, Provincia

# Constantes de descarga y carga
TIMEOUT = 30  # segundos (REQ-E8-007)
MAX_POR_PAGINA = 1000  # batch ≤ 1.000 (REQ-E8-004, REQ-E8-014)
BATCH_SIZE = 1000  # bulk_create en batches de 1.000 (REQ-E8-014)

# Directorio y archivos de fixtures (fuente primaria — REQ-E8-015, REQ-E8-018)
FIXTURES_DIR = Path(__file__).resolve().parent / 'fixtures' / 'georef'
FIXTURE_FILES = {
    'provincias': 'provincias.json',
    'municipios': 'municipios.json',
    'localidades': 'localidades.json',
}


class GeoRefError(Exception):
    """Error explícito de descarga/carga del catálogo GeoRef.

    Mensaje claro para el operador, sin stacktrace (REQ-E8-006, SEC-E8-004).
    """


def _validar_url_https(url):
    """Rechaza con error claro si la URL base no comienza con ``https://``.

    Defensa en profundidad (SEC-E8-001): la validación primaria vive en
    ``telepark/settings.py`` (fail-fast al arranque).
    """
    if not url.startswith('https://'):
        raise GeoRefError(
            f'GEOREF_API_URL debe ser HTTPS (recibido: {url!r}). '
            'URLs http:// o file:// están prohibidas (SEC-E8-001).'
        )


def _get_json(url, params):
    """GET con ``urllib.request``, timeout 30s.

    Error HTTP o JSON inválido → ``GeoRefError`` con mensaje claro
    (REQ-E8-006, SEC-E8-004).
    """
    query = urllib.parse.urlencode(params)
    full_url = f'{url}?{query}'
    try:
        with urllib.request.urlopen(full_url, timeout=TIMEOUT) as resp:
            payload = resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        raise GeoRefError(
            f'Error HTTP {e.code} al consultar GeoRef: {full_url}'
        ) from e
    except urllib.error.URLError as e:
        raise GeoRefError(
            f'Error de red al consultar GeoRef: {e.reason}'
        ) from e
    except TimeoutError as e:
        raise GeoRefError(
            f'Timeout ({TIMEOUT}s) al consultar GeoRef: {full_url}'
        ) from e

    try:
        return json.loads(payload)
    except json.JSONDecodeError as e:
        raise GeoRefError(
            f'Respuesta JSON inválida de GeoRef: {e}'
        ) from e


def _descargar_recurso(endpoint, campos, clave=None):
    """Descarga un recurso paginado con ``max=1000``/``inicio`` y ``orden=id``.

    ``clave`` es la key del payload JSON donde vive la lista de items; por
    defecto coincide con ``endpoint``. Algunos endpoints usan una clave distinta
    de su ruta (ej. ``/localidades-censales`` → payload ``localidades_censales``),
    por lo que la clave debe pasarse explícita para no retornar una lista vacía
    en silencio (REQ-11.1.2, REQ-11.1.4).

    Retorna la lista cruda de items de GeoRef (REQ-E8-004, REQ-E8-005).
    """
    url = settings.GEOREF_API_URL
    _validar_url_https(url)

    resultados = []
    inicio = 0
    while True:
        params = {
            'campos': campos,
            'max': MAX_POR_PAGINA,
            'inicio': inicio,
            'orden': 'id',
            'aplanar': 'true',
        }
        data = _get_json(f'{url}/{endpoint}', params)
        items = data.get(clave or endpoint, [])
        if not items:
            break
        resultados.extend(items)
        total = data.get('total', 0)
        inicio += len(items)
        if inicio >= total or len(items) < MAX_POR_PAGINA:
            break

    return resultados


def _normalizar_item(item, claves):
    """Normaliza un item de GeoRef al formato de fixture.

    Con ``aplanar=true`` la API suele devolver ``provincia_id``/``municipio_id``
    directos; si no, se extraen manualmente los anidados ``provincia.id`` /
    ``municipio.id`` (nota de normalización del plan, S-08).
    """
    normalizado = {clave: item[clave] for clave in claves if clave in item}

    if 'provincia_id' not in normalizado and isinstance(item.get('provincia'), dict):
        normalizado['provincia_id'] = item['provincia'].get('id')
    if 'municipio_id' not in normalizado and isinstance(item.get('municipio'), dict):
        normalizado['municipio_id'] = item['municipio'].get('id')

    return normalizado


def descargar_provincias():
    """Descarga provincias: ``campos=id,nombre`` → lista ``{id, nombre}``."""
    items = _descargar_recurso('provincias', 'id,nombre')
    return [_normalizar_item(i, ('id', 'nombre')) for i in items]


def descargar_municipios():
    """Descarga municipios: ``campos=id,nombre,provincia.id`` → ``{id, nombre, provincia_id}``."""
    items = _descargar_recurso('municipios', 'id,nombre,provincia.id')
    return [_normalizar_item(i, ('id', 'nombre', 'provincia_id')) for i in items]


def descargar_localidades():
    """Descarga localidades desde ``/localidades-censales`` (INDEC, fuente única — E11).

    ``campos=id,nombre,provincia.id,municipio.id``. La clave de payload es
    ``localidades_censales`` (guión bajo), distinta de la ruta del endpoint
    (guión) — se pasa explícita a ``_descargar_recurso`` (REQ-11.1.1, REQ-11.1.3).

    Retorna ``{id, nombre, provincia_id, municipio_id}`` con ``municipio_id``
    nullable (ejidos no colindantes — REQ-E8-025).
    """
    items = _descargar_recurso(
        'localidades-censales',
        'id,nombre,provincia.id,municipio.id',
        clave='localidades_censales',
    )
    return [_normalizar_item(i, ('id', 'nombre', 'provincia_id', 'municipio_id')) for i in items]


def _escribir_atomico(ruta, items):
    """Escribe JSON con sobreescritura atómica (archivo temporal + rename)."""
    fd, tmp_path = tempfile.mkstemp(dir=str(FIXTURES_DIR), suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, ruta)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def generar_fixtures(datos):
    """Escribe los 3 fixtures JSON ordenados por ID GeoRef (REQ-E8-020, REQ-E8-021).

    ``datos`` es un dict ``{'provincias': [...], 'municipios': [...], 'localidades': [...]}``.
    """
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    for clave, items in datos.items():
        ordenados = sorted(items, key=lambda x: x['id'])
        _escribir_atomico(FIXTURES_DIR / FIXTURE_FILES[clave], ordenados)


def leer_fixtures():
    """Lee los 3 fixtures locales y retorna los datos normalizados.

    Fuente primaria de carga (REQ-E8-015). Retorna ``None`` si algún fixture
    no existe o está vacío (→ fallback a la API).
    """
    datos = {}
    for clave, nombre in FIXTURE_FILES.items():
        ruta = FIXTURES_DIR / nombre
        if not ruta.exists():
            return None
        with open(ruta, encoding='utf-8') as f:
            items = json.load(f)
        if not items:
            return None
        datos[clave] = items
    return datos


def _bulk_create_en_batches(modelo, objetos):
    """``bulk_create`` en batches de 1.000 (REQ-E8-014)."""
    for i in range(0, len(objetos), BATCH_SIZE):
        modelo.objects.bulk_create(objetos[i:i + BATCH_SIZE])


def cargar_provincias(datos):
    """Persiste provincias vía ``bulk_create``; retorna el conteo."""
    provincias = [
        Provincia(id_georef=item['id'], nombre=item['nombre'])
        for item in datos['provincias']
    ]
    _bulk_create_en_batches(Provincia, provincias)
    return len(provincias)


def cargar_municipios(datos):
    """Persiste municipios resolviendo FK ``idprovincia`` por ``id_georef`` (REQ-E8-008)."""
    provincias_por_georef = {p.id_georef: p for p in Provincia.objects.all()}
    municipios = []
    for item in datos['municipios']:
        municipios.append(Municipio(
            id_georef=item['id'],
            nombre=item['nombre'],
            idprovincia=provincias_por_georef.get(item.get('provincia_id')),
        ))
    _bulk_create_en_batches(Municipio, municipios)
    return len(municipios)


def cargar_localidades(datos):
    """Persiste localidades resolviendo FK ``idmunicipio`` por ``id_georef``.

    ``municipio_id`` es nullable (REQ-E8-025); ``codigopostal`` se persiste en
    ``None`` porque la API GeoRef no expone código postal (S-02).
    """
    municipios_por_georef = {m.id_georef: m for m in Municipio.objects.all()}
    localidades = []
    for item in datos['localidades']:
        localidades.append(Localidad(
            id_georef=item['id'],
            nombre=item['nombre'],
            codigopostal=None,
            idmunicipio=municipios_por_georef.get(item.get('municipio_id')),
        ))
    _bulk_create_en_batches(Localidad, localidades)
    return len(localidades)


def cargar_catalogo(datos):
    """Orquesta la carga en el orden provincias → municipios → localidades.

    Retorna conteos determinísticos ``{'provincias': n, 'municipios': n, 'localidades': n}``
    (REQ-E8-008, REQ-E8-016). Debe ejecutarse dentro de ``transaction.atomic()``.
    """
    return {
        'provincias': cargar_provincias(datos),
        'municipios': cargar_municipios(datos),
        'localidades': cargar_localidades(datos),
    }