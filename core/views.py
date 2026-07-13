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
            "login": _safe_reverse("login", request, format),
            "create_user": _safe_reverse("create_user", request, format),
            "users": _safe_reverse("get_users", request, format),
            "update_user": _safe_reverse("update_user", request, format),
            "refresh_token": _safe_reverse("token_refresh", request, format),
            "change_role": _safe_reverse("change_user_role", request, format),
        }),
        "personas": _clean_dict({
            "persona": _safe_reverse("persona-list", request, format),
            "personaEp": _safe_reverse("personaEp-list", request, format),
            "personaP": _safe_reverse("personaP-list", request, format),
            "direccion": _safe_reverse("direccion-list", request, format),
            "tipoparentesco": _safe_reverse("tipoparentesco-list", request, format),
            "localidad": _safe_reverse("localidad-list", request, format),
            "municipio": _safe_reverse("municipio-list", request, format),
            "diagnostico_por_personaEp": _safe_reverse("personaEp-diagnostico", request, format),
            "evolucion_por_personaEp": _safe_reverse("personaEp-evolucion", request, format),
            "indicacion_por_personaEp": _safe_reverse("personaEp-indicacion", request, format),
            "os_por_personaEp": _safe_reverse("personaEp-os", request, format),
        }),
        "salud": _clean_dict({
            "diagnostico": _safe_reverse("diagnostico-list", request, format),
            "evolucion": _safe_reverse("evolucion-list", request, format),
            "enfermedad": _safe_reverse("enfermedad-list", request, format),
            "medicamento": _safe_reverse("medicamento-list", request, format),
            "indicacion": _safe_reverse("indicacionmedicamento-list", request, format),
        }),
        "eventos": _clean_dict({
            "evento": _safe_reverse("evento-list", request, format),
            "tipoevento": _safe_reverse("tipoevento-list", request, format),
        }),
        "obra_social": _clean_dict({
            "obrasocial": _safe_reverse("obrasocial-list", request, format),
            "os": _safe_reverse("os-list", request, format),
        }),
        "talleres": _clean_dict({
            "taller": _safe_reverse("taller-list", request, format),
            "clasetaller": _safe_reverse("clasetaller-list", request, format),
            "actividad": _safe_reverse("actividad-list", request, format),
            "actividadrealizada": _safe_reverse("actividadrealizada-list", request, format),
            "asistenciataller": _safe_reverse("asistenciataller-list", request, format),
            "comportamiento": _safe_reverse("comportamiento-list", request, format),
            "factorclase": _safe_reverse("factorclase-list", request, format),
            "factorglobal": _safe_reverse("factorglobal-list", request, format),
            "unidadobservacion": _safe_reverse("unidadobservacion-list", request, format),
            "variableuo": _safe_reverse("variableuo-list", request, format),
            "valorvariableuo": _safe_reverse("valorvariableuo-list", request, format),
        }),
        "system": _clean_dict({
            "health": _safe_reverse("health_check", request, format),
            "swagger": _safe_reverse("swagger-ui", request, format),
            "redoc": _safe_reverse("redoc", request, format),
            "schema": _safe_reverse("schema", request, format),
        }),
    })
