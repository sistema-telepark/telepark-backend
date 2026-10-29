from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
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
    TipoVinculo,
    Vinculo,
)
from .serializers import (
    DepartamentoSerializer,
    DireccionSerializer,
    LocalidadSerializer,
    PersonaEPSerializer,
    PersonaSerializer,
    ProvinciaSerializer,
    TipoVinculoSerializer,
    VinculoSerializer,
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


VALORES_ACTIVO = ('true', 'false')


def _valor_activo(request):
    """Traduce `?activo` a bool; `None` si el parámetro está ausente o no hay request."""
    if request is None or 'activo' not in request.query_params:
        return None
    valor = request.query_params.get('activo')
    if valor not in VALORES_ACTIVO:
        raise ValidationError({'detail': f'El parámetro "activo" debe ser "true" o "false" (recibido: "{valor}").'})
    return valor == 'true'


class ActivoFilterMixin:
    """Filtra por `?activo` con whitelist exacta y desactiva la paginación cuando filtra."""

    def get_queryset(self):
        qs = super().get_queryset()
        valor = _valor_activo(getattr(self, 'request', None))
        if valor is None:
            return qs
        return self.manager.filtrar_por_activo(valor)

    def paginate_queryset(self, queryset):
        if _valor_activo(getattr(self, 'request', None)) is not None:
            # Filtro válido → array plano (paginación desactivada).
            return None
        return super().paginate_queryset(queryset)


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='activo',
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
                description=(
                    'Filtra personas por estado activo (true/false exactos). Con filtro válido la respuesta es un array '
                    'plano completo (sin paginar); sin el parámetro se conserva el envelope paginado global.'
                ),
            ),
        ],
    ),
)
class PersonaViewSet(ActivoFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Persona.objects
    serializer_class = PersonaSerializer
    permission_classes = [AdminOnlyForDelete]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='activo',
                type=bool,
                location=OpenApiParameter.QUERY,
                required=False,
                description=(
                    'Filtra personas EP por estado activo (true/false exactos). Con filtro válido la respuesta es un '
                    'array plano completo (sin paginar); sin el parámetro se conserva el envelope paginado global.'
                ),
            ),
        ],
    ),
)
class PersonaEPViewSet(ActivoFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = PersonaEP.objects
    serializer_class = PersonaEPSerializer
    permission_classes = [AdminOnlyForDelete]

    def perform_destroy(self, instance):
        instance.persona_ptr.delete()


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
class TipoVinculoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = TipoVinculo.objects
    serializer_class = TipoVinculoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class VinculoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Vinculo.objects
    serializer_class = VinculoSerializer
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
