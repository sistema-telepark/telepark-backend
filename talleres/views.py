from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import CascadeFilterMixin, ModelPKMixin, NoPaginationMixin, auto_tag_schema_view
from core.schema import error_response

from .serializers import (
    TallerSerializer, EncuentroSerializer, ActividadSerializer,
    ActividadRealizadaSerializer, AsistenciaTallerSerializer,
    FactorClaseSerializer,
    FactorGlobalSerializer, UnidadObservacionSerializer,
    VariableUOSerializer, ValorVariableUOSerializer,
)
from .models import (
    Taller, Encuentro, Actividad, Actividadrealizada,
    Asistenciataller, Factorclase, Factorglobal,
    Unidadobservacion, Variableuo, Valorvariableuo,
)


@auto_tag_schema_view
class TallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Taller.objects
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            204: OpenApiResponse(description='Sin contenido'),
            409: error_response(409, 'No se puede eliminar un taller con encuentros o actividades asociados'),
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.validar_borrado()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@auto_tag_schema_view
class EncuentroViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Encuentro.objects
    serializer_class = EncuentroSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ActividadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Actividad.objects
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            204: OpenApiResponse(description='Sin contenido'),
            409: error_response(409, 'No se puede eliminar una actividad con registros de actividades realizadas'),
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.validar_borrado()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@auto_tag_schema_view
class ActividadRealizadaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Actividadrealizada.objects
    serializer_class = ActividadRealizadaSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class AsistenciaTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Asistenciataller.objects
    serializer_class = AsistenciaTallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="idencuentro",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra factores de clase por encuentro (FK idencuentro). Con filtro activo la respuesta es array plano.",
            ),
        ],
    ),
)
class FactorClaseViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Factorclase.objects
    serializer_class = FactorClaseSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'idencuentro': 'idencuentro'}


@auto_tag_schema_view
class FactorGlobalViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Factorglobal.objects
    serializer_class = FactorGlobalSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class UnidadObservacionViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Unidadobservacion.objects
    serializer_class = UnidadObservacionSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class VariableUOViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Variableuo.objects
    serializer_class = VariableUOSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="idasistenciataller",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Filtra valores de variable UO por asistencia de taller (FK idasistenciataller). Con filtro activo la respuesta es array plano.",
            ),
        ],
    ),
)
class ValorVariableUOViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Valorvariableuo.objects
    serializer_class = ValorVariableUOSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'idasistenciataller': 'idasistenciataller'}
