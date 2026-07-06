from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    DireccionSerializer, LocalidadSerializer,
    MunicipioSerializer, PersonaEpSerializer,
    PersonaSerializer, PersonaPSerializer, TipoparentescoSerializer,
)
from .services import (
    PersonaService, PersonaEpService, DireccionService,
    TipoParentescoService, LocalidadService, MunicipioService,
)


_persona_service = PersonaService()
_personaep_service = PersonaEpService()
_direccion_service = DireccionService()
_tipoparentesco_service = TipoParentescoService()
_localidad_service = LocalidadService()
_municipio_service = MunicipioService()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = _persona_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class PersonaEPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaEpSerializer
    queryset = _personaep_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class PersonaPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaPSerializer
    queryset = _personaep_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class LocalidadViewSet(viewsets.ModelViewSet):
    serializer_class = LocalidadSerializer
    queryset = _localidad_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    queryset = _direccion_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class TipoParentescoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoparentescoSerializer
    queryset = _tipoparentesco_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializer
    queryset = _municipio_service.listar()
    permission_classes = [IsAuthenticated]
