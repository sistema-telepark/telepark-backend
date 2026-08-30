"""Módulo de carga del catálogo geográfico GeoRef."""
import json
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from django.conf import settings

from .models import Localidad, Municipio, Provincia

TIMEOUT = 30  # segundos por petición
MAX_POR_PAGINA = 1000  # página de la API GeoRef
BATCH_SIZE = 1000  # bulk_create en batches

# Directorio y archivos de fixtures locales.
FIXTURES_DIR = Path(__file__).resolve().parent / 'fixtures' / 'georef'
FIXTURE_FILES = {
    'provincias': 'provincias.json',
    'municipios': 'municipios.json',
    'localidades': 'localidades.json',
}


class GeoRefError(Exception):
    """Error explícito de descarga/carga del catálogo GeoRef."""


def _validar_url_https(url):
    """Rechaza con error claro si la URL base no comienza con ``https://``."""
    if not url.startswith('https://'):
        raise GeoRefError(
            f'GEOREF_API_URL debe ser HTTPS (recibido: {url!r}). '
            'URLs http:// o file:// están prohibidas.'
        )


def _get_json(url, params):
    """GET con ``urllib.request``, timeout 30s.

    Error HTTP o JSON inválido → ``GeoRefError`` con mensaje claro
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
    en silencio.

    Retorna la lista cruda de items de GeoRef.
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
    ``municipio.id``.
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


def descargar_departamentos():
    """Descarga departamentos: ``campos=id,nombre,provincia.id`` → ``{id, nombre, provincia_id}``.

    Fuente del segundo nivel administrativo para provincias sin municipios.
    Sin cambios de modelo/API.
    """
    items = _descargar_recurso('departamentos', 'id,nombre,provincia.id')
    return [_normalizar_item(i, ('id', 'nombre', 'provincia_id')) for i in items]


def completar_municipios_con_departamentos(municipios, departamentos):
    """Merge departamentos como municipios solo para provincias con 0 municipios.

    Función pura determinística (sin tocar BD): detecta las provincias que ya
    tienen municipios a partir de ``municipios``, filtra los departamentos de las
    provincias restantes (sin municipios) y retorna ``municipios + filtrados``
    ordenados por ``id``. Los ``id_georef`` de departamentos (ej. ``78007``) no
    colisionan con municipios reales (prefijo provincial único, solo se cargan en
    provincias sin municipios).
    """
    provincias_con_municipios = {m['provincia_id'] for m in municipios}
    departamentos_filtrados = [
        d for d in departamentos
        if d['provincia_id'] not in provincias_con_municipios
    ]
    return sorted(municipios + departamentos_filtrados, key=lambda x: x['id'])


def descargar_municipios_completos():
    """Descarga municipios + departamentos de provincias sin municipios."""
    municipios = descargar_municipios()
    departamentos = descargar_departamentos()
    return completar_municipios_con_departamentos(municipios, departamentos)


def descargar_localidades():
    """Descarga localidades desde ``/localidades-censales`` (INDEC, fuente única).

    ``campos=id,nombre,provincia.id,municipio.id``. La clave de payload es
    ``localidades_censales`` (guión bajo), distinta de la ruta del endpoint
    (guión) — se pasa explícita a ``_descargar_recurso``.

    Retorna ``{id, nombre, provincia_id, municipio_id}`` con ``municipio_id``
    nullable (ejidos no colindantes).
    """
    items = _descargar_recurso(
        'localidades-censales',
        'id,nombre,provincia.id,municipio.id',
        clave='localidades_censales',
    )
    return [_normalizar_item(i, ('id', 'nombre', 'provincia_id', 'municipio_id')) for i in items]


def generar_localidades_sinteticas(localidades, municipios):
    """Crea localidades homónimas sintéticas para municipios sin localidad.

    Función pura determinística (sin tocar BD): para cada municipio sin localidad
    (y no CABA), genera una localidad con ``id_georef = f"{municipio_id}0000"`` (ej. municipio ``060707``
    → ``0607070000``; departamento ``78007`` → ``780070000``). Si el id sintético
    ya existe → ``GeoRefError`` claro, sin sobreescritura .
    Retorna ``localidades + sintéticas`` ordenadas por ``id``.
    """
    municipios_con_localidad = {
        l['municipio_id'] for l in localidades if l.get('municipio_id')
    }
    existentes = {l['id'] for l in localidades}
    sinteticas = []
    for m in municipios:
        if m['id'] in municipios_con_localidad:
            continue
        if m['provincia_id'] == '02':
            continue  # CABA: usa la única localidad censal del catálogo
        id_sintetico = f"{m['id']}0000"
        if id_sintetico in existentes:
            raise GeoRefError(
                f"Colisión de id_georef sintético {id_sintetico!r} "
                f"(municipio {m['id']!r} {m['nombre']!r}): ya existe una localidad "
                'con ese id. No se sobreescribe.'
            )
        sinteticas.append({
            'id': id_sintetico,
            'nombre': m['nombre'],
            'provincia_id': m['provincia_id'],
            'municipio_id': m['id'],
        })
        existentes.add(id_sintetico)
    return sorted(localidades + sinteticas, key=lambda x: x['id'])


def descargar_catalogo_completo():
    """Descarga el catálogo completo con completitud aplicada.

    Orquesta: provincias → municipios completos (con departamentos de provincias
    sin municipios) → localidades (+ homónimas sintéticas). Retorna el dict
    ``{'provincias': [...], 'municipios': [...], 'localidades': [...]}`` listo
    para ``generar_fixtures``/``cargar_catalogo`` (shapes de dict idénticos a los
    fixtures; ``cargar_*`` no cambian).
    """
    provincias = descargar_provincias()
    municipios = descargar_municipios_completos()
    localidades = descargar_localidades()
    localidades = generar_localidades_sinteticas(localidades, municipios)
    return {
        'provincias': provincias,
        'municipios': municipios,
        'localidades': localidades,
    }


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
    """Escribe los 3 fixtures JSON ordenados por ID GeoRef.

    ``datos`` es un dict ``{'provincias': [...], 'municipios': [...], 'localidades': [...]}``.
    """
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    for clave, items in datos.items():
        ordenados = sorted(items, key=lambda x: x['id'])
        _escribir_atomico(FIXTURES_DIR / FIXTURE_FILES[clave], ordenados)


def leer_fixtures():
    """Lee los 3 fixtures locales y retorna los datos normalizados.

    Fuente primaria de carga. Retorna ``None`` si algún fixture
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
    """``bulk_create`` en batches de 1.000."""
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
    """Persiste municipios resolviendo FK ``idprovincia`` por ``id_georef``."""
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

    ``municipio_id`` es nullable; ``codigopostal`` se persiste en
    ``None`` porque la API GeoRef no expone código postal.
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

    Retorna conteos determinísticos ``{'provincias': n, 'municipios': n, 'localidades': n}``.
    Debe ejecutarse dentro de ``transaction.atomic()``.
    """
    return {
        'provincias': cargar_provincias(datos),
        'municipios': cargar_municipios(datos),
        'localidades': cargar_localidades(datos),
    }


def verificar_completitud():
    """Verifica la completitud del catálogo en BD.

    Consulta ORM: reporta
    provincias sin municipios y municipios sin localidades. Las comunas de CABA
    se excluyen del conteo de municipios sin localidad.
    """
    provincias_sin_municipios = Provincia.objects.filter(municipio__isnull=True).count()
    municipios_sin_localidades = (
        Municipio.objects.filter(localidad__isnull=True)
        .exclude(idprovincia__id_georef='02')
        .count()
    )
    return {
        'provincias_sin_municipios': provincias_sin_municipios,
        'municipios_sin_localidades': municipios_sin_localidades,
        'ok': provincias_sin_municipios == 0 and municipios_sin_localidades == 0,
    }