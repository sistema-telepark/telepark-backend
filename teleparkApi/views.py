from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import DireccionSerializer, LocalidadSerializer, MunicipioSerializer, PersonaSerializer, TipoparentescoSerializer, PersonaEpSerializer
from .models import Direccion, Localidad, Municipio, Persona, PersonaEp, Tipoparentesco
from .handlers import CRUDHandlerStrategies
from .static import http_method
# from .permission import has_permission

@api_view([http_method.POST, http_method.GET])
@permission_classes([IsAuthenticated])
def persona_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, Persona, PersonaSerializer)

@api_view([http_method.POST])
@permission_classes([IsAuthenticated])
def direccion_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, Direccion, DireccionSerializer)

@api_view([http_method.POST])
@permission_classes([IsAuthenticated])
def personaEp_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, PersonaEp, PersonaEpSerializer)

@api_view([http_method.POST])
@permission_classes([IsAuthenticated])
def tipoParentesco_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, Tipoparentesco, TipoparentescoSerializer)

@api_view([http_method.GET])
@permission_classes([IsAuthenticated])
def localidad_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, Localidad, LocalidadSerializer)

@api_view([http_method.GET])
@permission_classes([IsAuthenticated])
def municipio_list(request):
    return CRUDHandlerStrategies.getStrategy(request.method).handle(request, Municipio, MunicipioSerializer)
