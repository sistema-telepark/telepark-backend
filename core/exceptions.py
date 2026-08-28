"""Excepciones de dominio tipadas para el manejo centralizado de errores."""


class InvalidCredentialsError(Exception):
    """Credenciales inválidas o usuario deshabilitado en login.

    Target: 401 `invalid_credentials`.
    """


class ConflictError(Exception):
    """Conflicto de estado de negocio (ej. degradar al último administrador).

    Target: 409 `conflict`.
    """


class ValidationError(Exception):
    """Error de validación de entrada de dominio.

    Acepta `str` o `dict` en `args[0]` (errores por campo).

    Target: 400 `validation_error`.
    """