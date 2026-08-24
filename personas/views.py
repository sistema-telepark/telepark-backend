from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import (
    CascadeFilterMixin, ModelPKMixin, NoPaginationMixin, auto_tag_schema_view,
)

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


def _resolver_localidades_por_provincia(valor):
    """Resuelve el id_georef de la provincia y filtra localidades por prefijo."""
    try:
        provincia = Provincia.objects.get(pk=valor)
    except Provincia.DoesNotExist:
        return {'pk__in': []}
    return {'id_georef__startswith': provincia.id_georef}


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
                name="idmunicipio",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra localidades por municipio (FK idmunicipio). Con filtro activo la respuesta es array plano.",
            ),
            OpenApiParameter(
                name="idprovincia",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra localidades por provincia vía prefijo id_georef (incluye ejidos). Con filtro activo la respuesta es array plano.",
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
        'idmunicipio': 'idmunicipio',
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
                description="Filtra municipios por provincia (FK idprovincia). Con filtro activo la respuesta es array plano.",
            ),
        ],
    ),
)
class MunicipioViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Municipio.objects
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'idprovincia': 'idprovincia'}


@auto_tag_schema_view
class ProvinciaViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Provincia.objects
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
