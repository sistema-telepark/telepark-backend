"""Módulo de carga del catálogo geográfico GeoRef."""
import json
import os
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from django.conf import settings

from .models import Departamento, Localidad, Provincia

TIMEOUT = 30  # segundos por petición
MAX_POR_PAGINA = 1000  # página de la API GeoRef
BATCH_SIZE = 1000  # bulk_create en batches

# Directorio y archivos de fixtures locales.
FIXTURES_DIR = Path(__file__).resolve().parent / 'fixtures' / 'georef'
FIXTURE_FILES = {
    'provincias': 'provincias.json',
    'departamentos': 'departamentos.json',
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
    defecto coincide con ``endpoint``.

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

    Con ``aplanar=true`` la API suele devolver ``provincia_id``/``departamento_id``
    directos; si no, se extraen manualmente los anidados ``provincia.id`` /
    ``departamento.id``.
    """
    normalizado = {clave: item[clave] for clave in claves if clave in item}

    if 'provincia_id' not in normalizado and isinstance(item.get('provincia'), dict):
        normalizado['provincia_id'] = item['provincia'].get('id')
    if 'departamento_id' not in normalizado and isinstance(item.get('departamento'), dict):
        normalizado['departamento_id'] = item['departamento'].get('id')

    return normalizado


def descargar_provincias():
    """Descarga provincias: ``campos=id,nombre`` → lista ``{id, nombre}``."""
    items = _descargar_recurso('provincias', 'id,nombre')
    return [_normalizar_item(i, ('id', 'nombre')) for i in items]


def descargar_departamentos():
    """Descarga departamentos: ``campos=id,nombre,provincia.id`` → ``{id, nombre, provincia_id}``."""
    items = _descargar_recurso('departamentos', 'id,nombre,provincia.id')
    return [_normalizar_item(i, ('id', 'nombre', 'provincia_id')) for i in items]


def descargar_localidades():
    """Descarga localidades censales desde ``/localidades-censales`` (INDEC).

    ``campos=id,nombre,provincia.id,provincia.nombre,departamento.id,departamento.nombre``.
    La clave de payload es ``localidades_censales``.

    Retorna ``{id, nombre, provincia_id, provincia_nombre, departamento_id, departamento_nombre}``.
    """
    items = _descargar_recurso(
        'localidades-censales',
        'id,nombre,provincia.id,provincia.nombre,departamento.id,departamento.nombre',
        clave='localidades_censales',
    )
    return [
        _normalizar_item(i, (
            'id', 'nombre', 'provincia_id', 'provincia_nombre',
            'departamento_id', 'departamento_nombre',
        ))
        for i in items
    ]


def descargar_asentamientos():
    """Descarga asentamientos desde ``/asentamientos`` (BAHRA).

    ``campos=id,nombre,provincia.id,departamento.id,departamento.nombre``. La
    clave de payload es ``asentamientos``.

    Retorna ``{id, nombre, provincia_id, departamento_id, departamento_nombre}``.
    """
    items = _descargar_recurso(
        'asentamientos',
        'id,nombre,provincia.id,departamento.id,departamento.nombre',
        clave='asentamientos',
    )
    return [
        _normalizar_item(i, ('id', 'nombre', 'provincia_id', 'departamento_id', 'departamento_nombre'))
        for i in items
    ]


def _resolver_departamento_censal(localidades, departamentos):
    """Pasada 1: cruce censal por ``(provincia_id, nombre)``.

    Indexa los departamentos por ``(provincia_id, nombre)`` y resuelve cada
    localidad censal. Solo se resuelve si hay exactamente un departamento
    candidato (la clave compuesta desambigua homónimos entre provincias; los
    duplicados dentro de una misma provincia quedan sin resolver).
    """
    indice = {}
    for d in departamentos:
        indice.setdefault((d['provincia_id'], d['nombre']), []).append(d['id'])

    for loc in localidades:
        clave = (loc.get('provincia_id'), loc.get('departamento_nombre'))
        candidatos = indice.get(clave, [])
        if len(candidatos) == 1:
            loc['departamento_id'] = candidatos[0]
            loc['fuente_departamento'] = 'censal'


def _resolver_departamento_bahra(localidades, asentamientos):
    """Pasada 2: fallback contra ``/asentamientos`` (BAHRA) por ``(provincia_id, nombre)``.

    Resuelve las localidades que quedaron sin departamento en la pasada censal,
    cruzando por nombre de localidad contra el nombre del asentamiento dentro de
    la misma provincia. Solo se resuelve si hay exactamente un candidato.
    """
    indice = {}
    for a in asentamientos:
        indice.setdefault((a['provincia_id'], a['nombre']), []).append(a['departamento_id'])

    for loc in localidades:
        if loc.get('fuente_departamento'):
            continue
        clave = (loc.get('provincia_id'), loc.get('nombre'))
        candidatos = indice.get(clave, [])
        if len(candidatos) == 1:
            loc['departamento_id'] = candidatos[0]
            loc['fuente_departamento'] = 'bahra'


def descargar_catalogo_completo():
    """Descarga el catálogo completo.

    Orquesta: provincias → departamentos → localidades-censales, y resuelve la
    FK ``iddepartamento`` de cada localidad por ``(provincia_id, nombre)`` en dos
    pasadas (cruce censal → fallback ``/asentamientos`` BAHRA). El remanente sin
    resolver queda con ``fuente_departamento='manual'`` y ``departamento_id=None``.

    Retorna el dict ``{'provincias': [...], 'departamentos': [...], 'localidades': [...]}``
    listo para ``generar_fixtures``/``cargar_catalogo``.
    """
    provincias = descargar_provincias()
    departamentos = descargar_departamentos()
    localidades = descargar_localidades()

    _resolver_departamento_censal(localidades, departamentos)
    pendientes = [loc for loc in localidades if not loc.get('fuente_departamento')]
    if pendientes:
        asentamientos = descargar_asentamientos()
        _resolver_departamento_bahra(localidades, asentamientos)

    for loc in localidades:
        if not loc.get('fuente_departamento'):
            loc['departamento_id'] = None
            loc['fuente_departamento'] = 'manual'

    return {
        'provincias': provincias,
        'departamentos': departamentos,
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

    ``datos`` es un dict ``{'provincias': [...], 'departamentos': [...], 'localidades': [...]}``.
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


def _upsert_catalogo(modelo, items, campos_extra=(), resolver=None):
    """Upsert por ``id_georef``: actualiza existentes y crea faltantes.

    ``items`` son dicts normalizados con ``id`` y ``nombre``. ``campos_extra``
    son campos adicionales a refrescar en registros existentes y ``resolver``
    setea campos/FK sobre cada instancia antes de persistir.
    """
    existentes = {m.id_georef: m for m in modelo.objects.all()}
    objetos = []
    for item in items:
        instancia = existentes.get(item['id'])
        if instancia is None:
            instancia = modelo(id_georef=item['id'], nombre=item['nombre'])
        else:
            instancia.nombre = item['nombre']
        if resolver is not None:
            resolver(instancia, item)
        objetos.append(instancia)

    nuevos = [o for o in objetos if o.pk is None]
    for i in range(0, len(nuevos), BATCH_SIZE):
        modelo.objects.bulk_create(nuevos[i:i + BATCH_SIZE], ignore_conflicts=True)

    a_actualizar = [o for o in objetos if o.pk is not None]
    campos = ('nombre',) + tuple(campos_extra)
    for i in range(0, len(a_actualizar), BATCH_SIZE):
        modelo.objects.bulk_update(a_actualizar[i:i + BATCH_SIZE], campos)

    return len(objetos)


def cargar_provincias(datos):
    """Upsert de provincias por ``id_georef``; retorna el conteo."""
    return _upsert_catalogo(Provincia, datos['provincias'])


def cargar_departamentos(datos):
    """Upsert de departamentos resolviendo FK ``idprovincia`` por ``id_georef``."""
    provincias_por_georef = {p.id_georef: p for p in Provincia.objects.all()}

    def resolver(instancia, item):
        instancia.idprovincia = provincias_por_georef.get(item.get('provincia_id'))

    return _upsert_catalogo(
        Departamento, datos['departamentos'], ('idprovincia',), resolver
    )


def cargar_localidades(datos):
    """Upsert de localidades resolviendo FK ``iddepartamento`` por ``id_georef``.

    ``codigopostal`` se persiste en ``None`` porque la API GeoRef no expone
    código postal. ``fuente_departamento`` se persiste tal cual viene en el item
    (``censal``/``bahra``/``manual``).
    """
    departamentos_por_georef = {d.id_georef: d for d in Departamento.objects.all()}

    def resolver(instancia, item):
        instancia.iddepartamento = departamentos_por_georef.get(item.get('departamento_id'))
        instancia.codigopostal = None
        instancia.fuente_departamento = item.get('fuente_departamento')

    return _upsert_catalogo(
        Localidad, datos['localidades'],
        ('iddepartamento', 'codigopostal', 'fuente_departamento'), resolver
    )


def cargar_catalogo(datos):
    """Orquesta la carga en el orden provincias → departamentos → localidades.

    Retorna conteos determinísticos ``{'provincias': n, 'departamentos': n, 'localidades': n}``.
    Debe ejecutarse dentro de ``transaction.atomic()``.
    """
    return {
        'provincias': cargar_provincias(datos),
        'departamentos': cargar_departamentos(datos),
        'localidades': cargar_localidades(datos),
    }
