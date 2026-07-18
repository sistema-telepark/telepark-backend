import logging

from django.http.response import JsonResponse
from rest_framework import status

logger = logging.getLogger(__name__)


class ExceptionMiddleware(object):
    """Middleware que captura excepciones no manejadas y retorna JSON.

    Las excepciones específicas (ValidationError, NotFound, etc.) ahora
    son manejadas por DRF directamente. Este middleware actúa como
    catch-all final para errores inesperados.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        logger.error(f"Unhandled exception: {repr(exception)}", exc_info=True)
        return JsonResponse(
            {'error': repr(exception)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
