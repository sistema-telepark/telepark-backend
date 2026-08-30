import logging
import uuid

from django.conf import settings
from django.http.response import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)


class ExceptionMiddleware(object):
    """Middleware catch-all final: responde 500 genérico y loguea el error."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.correlation_id = uuid.uuid4().hex[:12]
        return self.get_response(request)

    def process_exception(self, request, exception):
        correlation_id = getattr(request, 'correlation_id', None)
        logger.error(
            "Unhandled exception (correlation_id=%s): %s",
            correlation_id,
            type(exception).__name__,
            exc_info=settings.DEBUG,
        )
        return JsonResponse(
            {
                'detail': 'Error interno del servidor',
                'code': 'internal_error',
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )