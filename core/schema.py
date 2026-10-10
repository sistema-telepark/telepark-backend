"""Esquemas OpenAPI reutilizables para drf-spectacular.

Componentes de respuesta de error {detail, code, status} para referenciar en `extend_schema`.
"""

ERROR_4XX_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {
            'description': 'Mensaje descriptivo del error (string humano o dict por campo en validación)',
            'oneOf': [
                {'type': 'string'},
                {'type': 'object'},
            ],
        },
        'code': {
            'type': 'string',
            'description': 'Código semántico snake_case',
            'enum': [
                'validation_error',
                'parse_error',
                'not_authenticated',
                'invalid_credentials',
                'permission_denied',
                'not_found',
                'method_not_allowed',
                'not_acceptable',
                'unsupported_media_type',
                'throttled',
                'integrity_error',
                'conflict',
            ],
        },
        'status': {
            'type': 'integer',
            'description': 'Código HTTP, coincide con la línea de estado',
        },
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_500_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {
            'type': 'string',
            'description': 'Mensaje genérico: "Error interno del servidor"',
        },
        'code': {
            'type': 'string',
            'description': 'Código semántico: "internal_error"',
            'enum': ['internal_error'],
        },
        'status': {
            'type': 'integer',
            'description': 'Código HTTP: 500',
            'enum': [500],
        },
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_400_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {
            'oneOf': [
                {'type': 'string', 'description': 'Mensaje de error general'},
                {
                    'type': 'object',
                    'description': 'Errores por campo (ej. {"email": ["El email ya está registrado"]})',
                },
            ],
        },
        'code': {
            'type': 'string',
            'enum': ['validation_error', 'parse_error', 'integrity_error'],
        },
        'status': {'type': 'integer', 'enum': [400]},
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_401_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'},
        'code': {'type': 'string', 'enum': ['not_authenticated', 'invalid_credentials']},
        'status': {'type': 'integer', 'enum': [401]},
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_403_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'},
        'code': {'type': 'string', 'enum': ['permission_denied']},
        'status': {'type': 'integer', 'enum': [403]},
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_404_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'},
        'code': {'type': 'string', 'enum': ['not_found']},
        'status': {'type': 'integer', 'enum': [404]},
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_409_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string'},
        'code': {'type': 'string', 'enum': ['conflict']},
        'status': {'type': 'integer', 'enum': [409]},
    },
    'required': ['detail', 'code', 'status'],
}

ERROR_429_SCHEMA = {
    'type': 'object',
    'properties': {
        'detail': {'type': 'string', 'description': 'Tiempo de espera para realizar la siguiente petición'},
        'code': {'type': 'string', 'enum': ['throttled']},
        'status': {'type': 'integer', 'enum': [429]},
    },
    'required': ['detail', 'code', 'status'],
}


def error_response(code_http, description=None, schema=None):
    """Genera un OpenApiResponse para un código de error específico.

    Si no se especifica schema, usa el genérico ERROR_4XX_SCHEMA o ERROR_500_SCHEMA.
    """
    from drf_spectacular.utils import OpenApiResponse

    schemas_por_codigo = {
        400: ERROR_400_SCHEMA,
        401: ERROR_401_SCHEMA,
        403: ERROR_403_SCHEMA,
        404: ERROR_404_SCHEMA,
        409: ERROR_409_SCHEMA,
        429: ERROR_429_SCHEMA,
        500: ERROR_500_SCHEMA,
    }
    s = schema or schemas_por_codigo.get(code_http, ERROR_4XX_SCHEMA)
    return OpenApiResponse(response=s, description=description or f'Error {code_http}')


RESPONSE_SUCCESS_204 = {
    'type': 'object',
    'properties': {},
}


RUTAS_PUBLICAS = frozenset(
    {
        '/api/v1/health',
        '/api/v1/auth/login',
        '/api/v1/auth/refresh',
        '/schema/',
    }
)

_METODOS_HTTP = ('get', 'post', 'put', 'patch', 'delete', 'options', 'head')


def _respuesta_error(schema, description):
    return {'description': description, 'content': {'application/json': {'schema': schema}}}


def agregar_respuestas_autenticacion(result, generator, request, public):
    """Agrega 401/403 a las operaciones autenticadas; excluye health, login, refresh y schema."""
    for ruta, operaciones in result.get('paths', {}).items():
        if ruta in RUTAS_PUBLICAS:
            continue
        for metodo in _METODOS_HTTP:
            operacion = operaciones.get(metodo)
            if operacion is None:
                continue
            if not any('jwtAuth' in requisito for requisito in operacion.get('security', [])):
                continue
            respuestas = operacion.setdefault('responses', {})
            respuestas.setdefault('401', _respuesta_error(ERROR_401_SCHEMA, 'No autenticado'))
            respuestas.setdefault('403', _respuesta_error(ERROR_403_SCHEMA, 'Permiso denegado'))
    return result
