from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

from .serializers import (
    DireccionSerializer, LocalidadSerializer,
    MunicipioSerializer, PersonaEpSerializer,
    PersonaSerializer, ProvinciaSerializer,
    TipoparentescoSerializer,
)
from .models import (
    Persona, PersonaEp, Direccion,
    Tipoparentesco, Localidad, Municipio, Provincia,
)


@auto_tag_schema_view
class PersonaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Persona.objects
    serializer_class = PersonaSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class PersonaEPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = PersonaEp.objects
    serializer_class = PersonaEpSerializer
    permission_classes = [IsAuthenticated]

@auto_tag_schema_view
class LocalidadViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Localidad.objects
    serializer_class = LocalidadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class DireccionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Direccion.objects
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class TipoParentescoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Tipoparentesco.objects
    serializer_class = TipoparentescoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class MunicipioViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Municipio.objects
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ProvinciaViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Provincia.objects
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
