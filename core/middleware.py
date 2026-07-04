from django.http.response import JsonResponse
from rest_framework import status

class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse({ 'error': repr(exception) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
