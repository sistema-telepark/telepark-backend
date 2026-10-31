from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.exceptions import ValidationError
from core.mixins import CascadeFilterMixin, ModelPKMixin, NoPaginationMixin, auto_tag_schema_view
from core.schema import error_response

from .models import (
    Actividad,
    AsistenciaTaller,
    Encuentro,
    EncuentroActividad,
    EncuentroFactorGlobal,
    EncuentroTaller,
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
    EncuentroTallerSerializer,
    FactorGlobalSerializer,
    RosterAsistenciaSerializer,
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

    def get_queryset(self):
        return super().get_queryset().prefetch_related('talleres')


@auto_tag_schema_view
class EncuentroTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = EncuentroTaller.objects
    serializer_class = EncuentroTallerSerializer
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
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='encuentro',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra encuentros-actividades por encuentro (FK encuentro). Con filtro activo la respuesta es array plano.',
            ),
        ],
    ),
)
class EncuentroActividadViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = EncuentroActividad.objects
    serializer_class = EncuentroActividadSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'encuentro': 'encuentro'}


@auto_tag_schema_view
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='encuentro',
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Filtra asistencias de taller por encuentro (FK encuentro). Con filtro activo la respuesta es array plano.',
            ),
        ],
    ),
    update=extend_schema(
        responses={
            200: AsistenciaTallerSerializer,
            409: error_response(409, 'El par persona_ep + encuentro ya está ocupado por otra asistencia'),
        },
    ),
    partial_update=extend_schema(
        responses={
            200: AsistenciaTallerSerializer,
            409: error_response(409, 'El par persona_ep + encuentro ya está ocupado por otra asistencia'),
        },
    ),
)
class AsistenciaTallerViewSet(CascadeFilterMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = AsistenciaTaller.objects
    serializer_class = AsistenciaTallerSerializer
    permission_classes = [IsAuthenticated]
    cascade_lookups = {'encuentro': 'encuentro'}

    @extend_schema(
        summary='Registrar asistencia de taller',
        description=(
            'Upsert sobre el par `persona_ep` + `encuentro`: si no existe la asistencia se crea (201); '
            'si ya existe se actualiza únicamente `estado`, se conserva la fila y se responde 200.'
        ),
        responses={
            201: AsistenciaTallerSerializer,
            200: AsistenciaTallerSerializer,
            400: error_response(400, 'Datos inválidos'),
        },
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        datos = serializer.validated_data
        asistencia, creada = self.manager.registrar_asistencia(datos['persona_ep'], datos['encuentro'], datos['estado'])
        salida = self.get_serializer(asistencia)
        codigo = status.HTTP_201_CREATED if creada else status.HTTP_200_OK
        return Response(salida.data, status=codigo)

    def perform_update(self, serializer):
        actual = serializer.instance
        actual.validar_disponibilidad(
            serializer.validated_data.get('persona_ep', actual.persona_ep),
            serializer.validated_data.get('encuentro', actual.encuentro),
        )
        serializer.save()


@extend_schema(
    tags=['talleres'],
    responses={
        200: RosterAsistenciaSerializer(many=True),
        400: error_response(400, 'Identificador de encuentro no numérico'),
        404: error_response(404, 'Encuentro no encontrado'),
    },
)
class RosterEncuentroAsistenciasView(NoPaginationMixin, GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RosterAsistenciaSerializer
    queryset = AsistenciaTaller.objects.none()

    def get(self, request, encuentro_pk):
        try:
            encuentro_id = int(encuentro_pk)
        except TypeError, ValueError:
            raise ValidationError('El identificador del encuentro debe ser numérico') from None
        encuentro = Encuentro.objects.filter(pk=encuentro_id).first()
        if encuentro is None:
            raise NotFound('No encontrado')
        return Response(self.get_serializer(AsistenciaTaller.objects.listar_roster(encuentro), many=True).data)


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
