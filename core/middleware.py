from django.http.response import JsonResponse
from rest_framework import status
from core.exceptions import (
    ServiceException,
    NotFoundException,
    ValidationError,
    PermissionDeniedError,
    ConflictError,
    AuthenticationError,
)
import logging

logger = logging.getLogger(__name__)


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        error_mapping = {
            NotFoundException: status.HTTP_404_NOT_FOUND,
            ValidationError: status.HTTP_400_BAD_REQUEST,
            PermissionDeniedError: status.HTTP_403_FORBIDDEN,
            ConflictError: status.HTTP_409_CONFLICT,
            AuthenticationError: status.HTTP_401_UNAUTHORIZED,
        }

        for exc_type, http_status in error_mapping.items():
            if isinstance(exception, exc_type):
                return JsonResponse(
                    {'error': str(exception)},
                    status=http_status
                )

        logger.error(f"Unhandled exception: {repr(exception)}", exc_info=True)
        return JsonResponse(
            {'error': repr(exception)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
