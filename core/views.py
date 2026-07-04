from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError
from django.http import JsonResponse


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
