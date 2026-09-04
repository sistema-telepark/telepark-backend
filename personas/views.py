from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import (
    CascadeFilterMixin, ModelPKMixin, NoPaginationMixin, auto_tag_schema_view,
)

from .serializers import (
    DireccionSerializer, LocalidadSerializer,
    DepartamentoSerializer, PersonaEpSerializer,
    PersonaSerializer, ProvinciaSerializer,
    TipoparentescoSerializer,
)
from .models import (
    Persona, PersonaEp, Direccion,
    Tipoparentesco, Localidad, Departamento, Provincia,
)


def _resolver_localidades_por_provincia(valor):
    """Resuelve el filtro idprovincia vía join FK localidad → departamento → provincia."""
    try:
        Provincia.objects.get(pk=valor)
    except Provincia.DoesNotExist:
        return {'pk__in': []}
    return {'iddepartamento__idprovincia': valor}


def _resolver_localidades_por_departamento(valor):
    """Resuelve el filtro iddepartamento."""
    try:
        Departamento.objects.get(pk=valor)
    except Departamento.DoesNotExist:
        return {'pk__in': []}
    return {'iddepartamento': valor}


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
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="iddepartamento",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra localidades por departamento (FK iddepartamento). Con filtro activo la respuesta es array plano.",
            ),
            OpenApiParameter(
                name="idprovincia",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra localidades por provincia (FK departamento → provincia). Con filtro activo la respuesta es array plano.",
            ),
        ],
    ),
)
class LocalidadViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Localidad.objects
    serializer_class = LocalidadSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {
        'iddepartamento': _resolver_localidades_por_departamento,
        'idprovincia': _resolver_localidades_por_provincia,
    }


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
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="idprovincia",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra departamentos por provincia (FK idprovincia). Con filtro activo la respuesta es array plano.",
            ),
        ],
    ),
)
class DepartamentoViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Departamento.objects
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'idprovincia': 'idprovincia'}


@auto_tag_schema_view
class ProvinciaViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Provincia.objects
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
