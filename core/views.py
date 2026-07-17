from django.conf import settings
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.urls.exceptions import NoReverseMatch
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema


class ApiRootPermission(BasePermission):
    """AllowAny en dev, IsAuthenticated en prod."""
    def has_permission(self, request, view):
        if settings.DEBUG:
            return True
        return request.user and request.user.is_authenticated


def _safe_reverse(name, request, format=None):
    try:
        return reverse(name, request=request, format=format)
    except NoReverseMatch:
        return None


def _clean_dict(d):
    return {k: v for k, v in d.items() if v is not None}


@extend_schema(
    tags=['sistema'],
    description="Verifica el estado de conexion a la base de datos y cuenta las tablas de negocio.",
    responses={
        200: {"type": "object", "properties": {"status": {"type": "string"}, "database": {"type": "string"}, "tables": {"type": "integer"}}},
        503: {"type": "object", "properties": {"status": {"type": "string"}, "database": {"type": "string"}, "detail": {"type": "string"}}},
    },
)
@api_view(["GET"])
def health_check(request):
    result = {
        "status": "ok",
        "database": "unknown",
        "detail": None,
    }
    try:
        db_conn = connections[DEFAULT_DB_ALIAS]
        db_conn.ensure_connection()
        all_tables = db_conn.introspection.table_names()
        business_tables = [
            t for t in all_tables
            if not t.startswith('auth_') and not t.startswith('django_')
        ]
        result["database"] = "connected"
        result["tables"] = len(business_tables)
        return JsonResponse(result, status=200)
    except OperationalError:
        result["status"] = "error"
        result["database"] = "disconnected"
        result["detail"] = "Database connection failed"
        return JsonResponse(result, status=503)
    except Exception:
        result["status"] = "error"
        result["database"] = "disconnected"
        result["detail"] = "Health check failed"
        return JsonResponse(result, status=503)


def custom_404_view(request, exception=None):
    """Handler 404 personalizado con mensajes en español para REQ-VRS-09.

    Responde con JSON detallando la ruta solicitada y, cuando es una ruta
    legacy conocida, sugiere el endpoint equivalente en /api/v1/.
    """
    path = getattr(request, 'path', '')

    # Mapa de rutas legacy conocidas → sugerencia
    LEGACY_ROUTES = {
        '/api/v1/update_user': 'Para crear o actualizar usuarios use POST/PUT /api/v1/usuarios',
        '/api/v1/create_user': 'Para crear usuarios use POST /api/v1/usuarios',
        '/api/v1/delete_user': 'Para eliminar usuarios use DELETE /api/v1/usuarios/{username}',
        '/api/v1/get_user': 'Para obtener usuarios use GET /api/v1/usuarios o GET /api/v1/usuarios/{username}',
        '/api/v1/login': 'Para autenticarse use POST /api/v1/auth/login',
        '/api/v1/refresh': 'Para renovar el token use POST /api/v1/auth/refresh',
        '/api/v1/register': 'Para registrar usuarios use POST /api/v1/usuarios',
        '/api/os': 'Para consultar obras sociales use GET /api/v1/obras-sociales',
        '/api/v1/os': 'Para consultar obras sociales use GET /api/v1/obras-sociales',
        '/api/v1/personasEp': 'Para consultar personas use GET /api/v1/personas-ep',
        '/api/v1/personaEp': 'Para consultar personas use GET /api/v1/personas-ep',
        '/api/v1/users': 'Para gestionar usuarios use /api/v1/usuarios',
    }

    suggestion = LEGACY_ROUTES.get(path)
    if suggestion:
        detail = (
            f"La ruta '{path}' ya no existe en la nueva estructura. "
            f"{suggestion}."
        )
    else:
        detail = (
            f"La ruta solicitada no existe en la API versionada /api/v1/"
        )

    return JsonResponse({"detail": detail}, status=404)


@extend_schema(
    tags=['sistema'],
    description=(
        "Root endpoint del API. Lista todos los recursos disponibles "
        "agrupados por modulo."
    ),
    responses={200: dict},
)
@api_view(["GET"])
@permission_classes([ApiRootPermission])
def api_root(request, format=None):
    return Response({
        "auth": _clean_dict({
            "login": _safe_reverse("auth-login", request, format),
            "refresh_token": _safe_reverse("auth-refresh", request, format),
            "usuarios": _safe_reverse("usuarios-list", request, format),
        }),
        "personas": _clean_dict({
            "personas": _safe_reverse("personas-list", request, format),
            "personas_ep": _safe_reverse("personas-ep-list", request, format),
            "direcciones": _safe_reverse("direcciones-list", request, format),
            "tipos_parentesco": _safe_reverse("tipos-parentesco-list", request, format),
            "localidades": _safe_reverse("localidades-list", request, format),
            "municipios": _safe_reverse("municipios-list", request, format),
            "diagnosticos_por_persona_ep": _safe_reverse("personas-ep-diagnosticos", request, format),
            "evoluciones_por_persona_ep": _safe_reverse("personas-ep-evoluciones", request, format),
            "indicaciones_por_persona_ep": _safe_reverse("personas-ep-indicaciones", request, format),
            "coberturas_por_persona_ep": _safe_reverse("personas-ep-coberturas", request, format),
        }),
        "salud": _clean_dict({
            "diagnosticos": _safe_reverse("diagnosticos-list", request, format),
            "evoluciones": _safe_reverse("evoluciones-list", request, format),
            "enfermedades": _safe_reverse("enfermedades-list", request, format),
            "medicamentos": _safe_reverse("medicamentos-list", request, format),
            "indicaciones": _safe_reverse("indicaciones-list", request, format),
        }),
        "eventos": _clean_dict({
            "eventos": _safe_reverse("eventos-list", request, format),
            "tipos_evento": _safe_reverse("tipos-evento-list", request, format),
        }),
        "obra_social": _clean_dict({
            "obras_sociales": _safe_reverse("obras-sociales-list", request, format),
            "coberturas": _safe_reverse("coberturas-list", request, format),
        }),
        "talleres": _clean_dict({
            "talleres": _safe_reverse("talleres-list", request, format),
            "clases_taller": _safe_reverse("clases-taller-list", request, format),
            "actividades": _safe_reverse("actividades-list", request, format),
            "actividades_realizadas": _safe_reverse("actividades-realizadas-list", request, format),
            "asistencias_taller": _safe_reverse("asistencias-taller-list", request, format),
            "comportamientos": _safe_reverse("comportamientos-list", request, format),
            "factores_clase": _safe_reverse("factores-clase-list", request, format),
            "factores_globales": _safe_reverse("factores-globales-list", request, format),
            "unidades_observacion": _safe_reverse("unidades-observacion-list", request, format),
            "variables_uo": _safe_reverse("variables-uo-list", request, format),
            "valores_variable_uo": _safe_reverse("valores-variable-uo-list", request, format),
        }),
        "system": _clean_dict({
            "health": _safe_reverse("health-check", request, format),
            "swagger": _safe_reverse("swagger-ui", request, format),
            "redoc": _safe_reverse("redoc", request, format),
            "schema": _safe_reverse("schema", request, format),
        }),
    })
