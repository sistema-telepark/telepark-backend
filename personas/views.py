from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin

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
class PersonaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _persona_service
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _persona_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class PersonaEPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _personaep_service
    serializer_class = PersonaEpSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _personaep_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class PersonaPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _personaep_service
    serializer_class = PersonaPSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _personaep_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class LocalidadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _localidad_service
    serializer_class = LocalidadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _localidad_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class DireccionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _direccion_service
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _direccion_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class TipoParentescoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _tipoparentesco_service
    serializer_class = TipoparentescoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _tipoparentesco_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['personas']),
    retrieve=extend_schema(tags=['personas']),
    create=extend_schema(tags=['personas']),
    update=extend_schema(tags=['personas']),
    partial_update=extend_schema(tags=['personas']),
    destroy=extend_schema(tags=['personas']),
)
class MunicipioViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _municipio_service
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _municipio_service.listar()
