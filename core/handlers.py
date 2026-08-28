"""Custom EXCEPTION_HANDLER de DRF — normaliza errores a {detail, code, status}."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

from core.exceptions import (
    ConflictError,
    InvalidCredentialsError,
    ValidationError as DomainValidationError,
)

# Normalización de `default_code` de DRF/simplejwt → taxonomía cerrada.
_CODE_NORMALIZACION = {
    'invalid': 'validation_error',
    'authentication_failed': 'not_authenticated',
    'token_not_valid': 'not_authenticated',
}

DETAIL_NOT_AUTHENTICATED = 'Credenciales de autenticación no provistas.'
DETAIL_INVALID_CREDENTIALS = 'Credenciales inválidas'
DETAIL_NOT_FOUND = 'No encontrado'
DETAIL_INTEGRITY_ERROR = 'Violación de integridad de datos'


def _normalizar_code(exc):
    code = getattr(exc, 'default_code', None) or 'error'
    return _CODE_NORMALIZACION.get(code, code)


def custom_exception_handler(exc, context):
    """Traduce una excepción a una Response normalizada, o None si no la conoce."""
    # Paso 1: delegar en el handler default de DRF (APIException, Http404, PermissionDenied).
    response = drf_exception_handler(exc, context)
    if response is not None:
        data = response.data
        if isinstance(data, dict) and 'detail' in data:
            detail = data['detail']
        else:
            detail = data
        code = _normalizar_code(exc)
        if isinstance(exc, NotAuthenticated):
            detail = DETAIL_NOT_AUTHENTICATED
        response.data = {
            'detail': detail,
            'code': code,
            'status': response.status_code,
        }
        return response

    # Paso 2: mapear el conjunto cerrado de excepciones de dominio.
    if isinstance(exc, InvalidCredentialsError):
        return Response(
            {'detail': DETAIL_INVALID_CREDENTIALS, 'code': 'invalid_credentials', 'status': 401},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if isinstance(exc, ConflictError):
        return Response(
            {'detail': str(exc), 'code': 'conflict', 'status': 409},
            status=status.HTTP_409_CONFLICT,
        )
    if isinstance(exc, DomainValidationError):
        detail = exc.args[0] if exc.args else 'Datos inválidos'
        return Response(
            {'detail': detail, 'code': 'validation_error', 'status': 400},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if isinstance(exc, LookupError):
        return Response(
            {'detail': str(exc), 'code': 'not_found', 'status': 404},
            status=status.HTTP_404_NOT_FOUND,
        )
    if isinstance(exc, PermissionError):
        return Response(
            {'detail': str(exc), 'code': 'permission_denied', 'status': 403},
            status=status.HTTP_403_FORBIDDEN,
        )
    if isinstance(exc, ObjectDoesNotExist):
        # Incluye `MultipleObjectsReturned` (subclase).
        return Response(
            {'detail': DETAIL_NOT_FOUND, 'code': 'not_found', 'status': 404},
            status=status.HTTP_404_NOT_FOUND,
        )
    if isinstance(exc, IntegrityError):
        return Response(
            {'detail': DETAIL_INTEGRITY_ERROR, 'code': 'integrity_error', 'status': 400},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Paso 3: excepción no mapeada → propaga al ExceptionMiddleware (500 genérico).
    return None