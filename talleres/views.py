from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.mixins import CascadeFilterMixin, ModelPKMixin, NoPaginationMixin, auto_tag_schema_view
from core.schema import error_response

from .models import (
    Actividad,
    AsistenciaTaller,
    Encuentro,
    EncuentroActividad,
    EncuentroFactorGlobal,
    FactorGlobal,
    Taller,
    UnidadObservacion,
    ValorVariableUO,
    VariableUO,
)
from .serializers import (
    ActividadSerializer,
    AsistenciaTallerSerializer,
    EncuentroActividadSerializer,
    EncuentroFactorGlobalSerializer,
    EncuentroSerializer,
    FactorGlobalSerializer,
    TallerSerializer,
    UnidadObservacionSerializer,
    ValorVariableUOSerializer,
    VariableUOSerializer,
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
class EncuentroActividadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = EncuentroActividad.objects
    serializer_class = EncuentroActividadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class AsistenciaTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = AsistenciaTaller.objects
    serializer_class = AsistenciaTallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='encuentro',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra encuentros-factores-globales por encuentro (FK encuentro). Con filtro activo la respuesta es array plano.',
            ),
        ],
    ),
)
class EncuentroFactorGlobalViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = EncuentroFactorGlobal.objects
    serializer_class = EncuentroFactorGlobalSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'encuentro': 'encuentro'}


@auto_tag_schema_view
class FactorGlobalViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = FactorGlobal.objects
    serializer_class = FactorGlobalSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class UnidadObservacionViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = UnidadObservacion.objects
    serializer_class = UnidadObservacionSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class VariableUOViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = VariableUO.objects
    serializer_class = VariableUOSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='asistencia_taller',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra valores de variable UO por asistencia de taller (FK asistencia_taller). Con filtro activo la respuesta es array plano.',
            ),
            OpenApiParameter(
                name='encuentro_actividad',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra valores de variable UO por encuentro-actividad (FK encuentro_actividad). Con filtro activo la respuesta es array plano.',
            ),
        ],
    ),
)
class ValorVariableUOViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = ValorVariableUO.objects
    serializer_class = ValorVariableUOSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'asistencia_taller': 'asistencia_taller', 'encuentro_actividad': 'encuentro_actividad'}
