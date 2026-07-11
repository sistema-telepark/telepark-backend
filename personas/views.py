from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

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


@auto_tag_schema_view
class PersonaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _persona_service
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class PersonaEPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _personaep_service
    serializer_class = PersonaEpSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class PersonaPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _personaep_service
    serializer_class = PersonaPSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class LocalidadViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _localidad_service
    serializer_class = LocalidadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class DireccionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _direccion_service
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class TipoParentescoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _tipoparentesco_service
    serializer_class = TipoparentescoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class MunicipioViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    service = _municipio_service
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]
