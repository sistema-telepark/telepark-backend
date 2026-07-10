from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin

from .serializers import (
    TallerSerializer, ClaseTallerSerializer, ActividadSerializer,
    ActividadRealizadaSerializer, AsistenciaTallerSerializer,
    ComportamientoSerializer, FactorClaseSerializer,
    FactorGlobalSerializer, UnidadObservacionSerializer,
    VariableUOSerializer, ValorVariableUOSerializer,
)
from .services import (
    TallerService, ClaseTallerService, ActividadService,
    ActividadRealizadaService, AsistenciaTallerService,
    ComportamientoService, FactorClaseService,
    FactorGlobalService, UnidadObservacionService,
    VariableUOService, ValorVariableUOService,
)


_taller_service = TallerService()
_clasetaller_service = ClaseTallerService()
_actividad_service = ActividadService()
_actividadrealizada_service = ActividadRealizadaService()
_asistenciataller_service = AsistenciaTallerService()
_comportamiento_service = ComportamientoService()
_factorclase_service = FactorClaseService()
_factorglobal_service = FactorGlobalService()
_unidadobservacion_service = UnidadObservacionService()
_variableuo_service = VariableUOService()
_valorvariableuo_service = ValorVariableUOService()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class TallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _taller_service
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _taller_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ClaseTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _clasetaller_service
    serializer_class = ClaseTallerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _clasetaller_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ActividadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _actividad_service
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _actividad_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ActividadRealizadaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _actividadrealizada_service
    serializer_class = ActividadRealizadaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _actividadrealizada_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class AsistenciaTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _asistenciataller_service
    serializer_class = AsistenciaTallerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _asistenciataller_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ComportamientoViewSet(ModelPKMixin, viewsets.ModelViewSet):
    pagination_class = None
    service = _comportamiento_service
    serializer_class = ComportamientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _comportamiento_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class FactorClaseViewSet(ModelPKMixin, viewsets.ModelViewSet):
    pagination_class = None
    service = _factorclase_service
    serializer_class = FactorClaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _factorclase_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class FactorGlobalViewSet(ModelPKMixin, viewsets.ModelViewSet):
    pagination_class = None
    service = _factorglobal_service
    serializer_class = FactorGlobalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _factorglobal_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class UnidadObservacionViewSet(ModelPKMixin, viewsets.ModelViewSet):
    pagination_class = None
    service = _unidadobservacion_service
    serializer_class = UnidadObservacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _unidadobservacion_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class VariableUOViewSet(ModelPKMixin, viewsets.ModelViewSet):
    pagination_class = None
    service = _variableuo_service
    serializer_class = VariableUOSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _variableuo_service.listar()


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ValorVariableUOViewSet(ModelPKMixin, viewsets.ModelViewSet):
    service = _valorvariableuo_service
    serializer_class = ValorVariableUOSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _valorvariableuo_service.listar()
