import re

from django.db.models import Prefetch
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import (
    CascadeFilterMixin,
    ModelPKMixin,
    NoPaginationMixin,
    PersonaEPSubresourceMixin,
    auto_tag_schema_view,
)
from core.permission import AdminOnlyForDelete
from core.schema import error_response

from .managers import CAMPOS_ORDEN_PERSONA
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
    VinculoOrdenSerializer,
    VinculoSerializer,
)
from .services import reordenar_vinculos

_NUMERIC_RE = re.compile(r'^-?\d+$')


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

VALORES_ORDERING = {campo: (campo, False) for campo in CAMPOS_ORDEN_PERSONA}
VALORES_ORDERING |= {f'-{campo}': (campo, True) for campo in CAMPOS_ORDEN_PERSONA}


def _valor_activo(request):
    """Traduce `?activo` a bool; `None` si el parámetro está ausente o no hay request."""
    if request is None or 'activo' not in request.query_params:
        return None
    valor = request.query_params.get('activo')
    if valor not in VALORES_ACTIVO:
        raise ValidationError({'detail': f'El parámetro "activo" debe ser "true" o "false" (recibido: "{valor}").'})
    return valor == 'true'


def _valor_ordering(request):
    """Traduce `?ordering` a (campo, descendente); `None` si está ausente o no hay request."""
    if request is None or 'ordering' not in request.query_params:
        return None
    valor = request.query_params.get('ordering')
    orden = VALORES_ORDERING.get(valor)
    if orden is None:
        opciones = ', '.join(VALORES_ORDERING)
        raise ValidationError({'detail': f'El parámetro "ordering" debe ser uno de: {opciones} (recibido: "{valor}").'})
    return orden


class ActivoFilterMixin:
    """Filtra por `?activo`, ordena por `?ordering` y desactiva la paginación cuando filtra."""

    def get_queryset(self):
        request = getattr(self, 'request', None)
        qs = super().get_queryset()
        valor = _valor_activo(request)
        if valor is not None:
            qs = self.manager.filtrar_por_activo(valor)
        orden = _valor_ordering(request)
        if orden is not None:
            campo, descendente = orden
            qs = self.manager.ordenar_por(campo, descendente, qs)
        return qs

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
            OpenApiParameter(
                name='ordering',
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=list(VALORES_ORDERING),
                description=(
                    'Ordena personas por apellido o nombre; el prefijo "-" invierte la dirección. Aplica tanto al '
                    'envelope paginado como al array plano con "activo". Sin el parámetro se conserva el orden por PK.'
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
            OpenApiParameter(
                name='ordering',
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                enum=list(VALORES_ORDERING),
                description=(
                    'Ordena personas EP por apellido o nombre; el prefijo "-" invierte la dirección. Aplica tanto al '
                    'envelope paginado como al array plano con "activo". Sin el parámetro se conserva el orden por PK.'
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

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related(
            Prefetch('vinculos', queryset=Vinculo.objects.listar_orden_llamada(), to_attr='vinculos_ordenados')
        )

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
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='persona_ep',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra vínculos por persona EP. La respuesta es siempre un array plano.',
            ),
        ],
    ),
)
class VinculoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'personas'
    manager = Vinculo.objects
    serializer_class = VinculoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        request = getattr(self, 'request', None)
        if request is None:
            return qs
        valor = request.query_params.get('persona_ep')
        if valor is None or valor == '':
            return qs
        if _NUMERIC_RE.match(valor) is None:
            raise ValidationError(
                {'detail': f'El parámetro "persona_ep" debe ser un ID numérico (recibido: "{valor}").'}
            )
        return qs.filter(persona_ep=valor)


@extend_schema(
    tags=['personas'],
    description=(
        'Reemplaza el orden de llamada de los vínculos del paciente. El body debe incluir exactamente los '
        'vínculos del paciente en el orden de llamada deseado (posiciones 1..N).'
    ),
    request=VinculoOrdenSerializer,
    responses={
        204: OpenApiResponse(description='Orden de llamada actualizado'),
        400: error_response(400, 'Payload inválido o identificador de persona no numérico'),
        401: error_response(401, 'No autenticado'),
        404: error_response(404, 'PersonaEP no encontrada'),
    },
)
class PersonaEPVinculosOrdenView(PersonaEPSubresourceMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VinculoOrdenSerializer
    queryset = Vinculo.objects.none()

    def put(self, request, persona_ep_pk):
        self.validar_persona_ep(persona_ep_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reordenar_vinculos(int(persona_ep_pk), serializer.validated_data['vinculos'])
        return Response(status=status.HTTP_204_NO_CONTENT)


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
