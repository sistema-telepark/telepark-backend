from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import (
    CascadeFilterMixin,
    ModelPKMixin,
    NoPaginationMixin,
    auto_tag_schema_view,
)
from core.permission import AdminOnlyForDelete

from .models import (
    Departamento,
    Direccion,
    Localidad,
    Persona,
    PersonaEP,
    Provincia,
    TipoParentesco,
)
from .serializers import (
    DepartamentoSerializer,
    DireccionSerializer,
    LocalidadSerializer,
    PersonaEPSerializer,
    PersonaSerializer,
    ProvinciaSerializer,
    TipoParentescoSerializer,
)


def _resolver_localidades_por_provincia(valor):
    """Resuelve el filtro provincia vía join FK localidad → departamento → provincia."""
    try:
        Provincia.objects.get(pk=valor)
    except Provincia.DoesNotExist:
        return {'pk__in': []}
    return {'departamento__provincia': valor}


def _resolver_localidades_por_departamento(valor):
    """Resuelve el filtro departamento."""
    try:
        Departamento.objects.get(pk=valor)
    except Departamento.DoesNotExist:
        return {'pk__in': []}
    return {'departamento': valor}


@auto_tag_schema_view
class PersonaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Persona.objects
    serializer_class = PersonaSerializer
    permission_classes = [AdminOnlyForDelete]


@auto_tag_schema_view
class PersonaEPViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = PersonaEP.objects
    serializer_class = PersonaEPSerializer
    permission_classes = [AdminOnlyForDelete]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='departamento',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra localidades por departamento (FK departamento). Con filtro activo la respuesta es array plano.',
            ),
            OpenApiParameter(
                name='provincia',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra localidades por provincia (FK departamento → provincia). Con filtro activo la respuesta es array plano.',
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
        'departamento': _resolver_localidades_por_departamento,
        'provincia': _resolver_localidades_por_provincia,
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
    manager = TipoParentesco.objects
    serializer_class = TipoParentescoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='provincia',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra departamentos por provincia (FK provincia). Con filtro activo la respuesta es array plano.',
            ),
        ],
    ),
)
class DepartamentoViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Departamento.objects
    serializer_class = DepartamentoSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'provincia': 'provincia'}


@auto_tag_schema_view
class ProvinciaViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Provincia.objects
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
