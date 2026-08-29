"""Esquemas OpenAPI reutilizables para drf-spectacular.

Componentes de respuesta de error {detail, code, status} para referenciar en `extend_schema`.
"""


# --- Componentes de respuesta de error ---

ERROR_4XX_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {
            "description": "Mensaje descriptivo del error (string humano o dict por campo en validación)",
            "oneOf": [
                {"type": "string"},
                {"type": "object"},
            ],
        },
        "code": {
            "type": "string",
            "description": "Código semántico snake_case (taxonomía cerrada)",
            "enum": [
                "validation_error",
                "parse_error",
                "not_authenticated",
                "invalid_credentials",
                "permission_denied",
                "not_found",
                "method_not_allowed",
                "not_acceptable",
                "unsupported_media_type",
                "throttled",
                "integrity_error",
                "conflict",
            ],
        },
        "status": {
            "type": "integer",
            "description": "Código HTTP, coincide con la línea de estado",
        },
    },
    "required": ["detail", "code", "status"],
}

ERROR_500_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {
            "type": "string",
            "description": "Mensaje genérico: \"Error interno del servidor\"",
        },
        "code": {
            "type": "string",
            "description": "Código semántico: \"internal_error\"",
            "enum": ["internal_error"],
        },
        "status": {
            "type": "integer",
            "description": "Código HTTP: 500",
            "enum": [500],
        },
    },
    "required": ["detail", "code", "status"],
}

# Componentes específicos por código para mayor claridad en Swagger
ERROR_400_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {
            "oneOf": [
                {"type": "string", "description": "Mensaje de error general"},
                {
                    "type": "object",
                    "description": "Errores por campo (ej. {\"email\": [\"El email ya está registrado\"]})",
                },
            ],
        },
        "code": {
            "type": "string",
            "enum": ["validation_error", "parse_error", "integrity_error"],
        },
        "status": {"type": "integer", "enum": [400]},
    },
    "required": ["detail", "code", "status"],
}

ERROR_401_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
        "code": {"type": "string", "enum": ["not_authenticated", "invalid_credentials"]},
        "status": {"type": "integer", "enum": [401]},
    },
    "required": ["detail", "code", "status"],
}

ERROR_403_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
        "code": {"type": "string", "enum": ["permission_denied"]},
        "status": {"type": "integer", "enum": [403]},
    },
    "required": ["detail", "code", "status"],
}

ERROR_404_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
        "code": {"type": "string", "enum": ["not_found"]},
        "status": {"type": "integer", "enum": [404]},
    },
    "required": ["detail", "code", "status"],
}

ERROR_409_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {"type": "string"},
        "code": {"type": "string", "enum": ["conflict"]},
        "status": {"type": "integer", "enum": [409]},
    },
    "required": ["detail", "code", "status"],
}

ERROR_429_SCHEMA = {
    "type": "object",
    "properties": {
        "detail": {"type": "string", "description": "Tiempo de espera para realizar la siguiente petición"},
        "code": {"type": "string", "enum": ["throttled"]},
        "status": {"type": "integer", "enum": [429]},
    },
    "required": ["detail", "code", "status"],
}


# --- Helpers para usar en extend_schema ---

def error_response(code_http, description=None, schema=None):
    """Genera un OpenApiResponse para un código de error específico.

    Si no se especifica schema, usa el genérico ERROR_4XX_SCHEMA o ERROR_500_SCHEMA.
    """
    from rest_framework.exceptions import ValidationError
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
    return OpenApiResponse(response=s, description=description or f"Error {code_http}")


# --- Componentes de respuesta comunes ---

RESPONSE_SUCCESS_204 = {
    "type": "object",
    "properties": {},
}
