from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

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
class TallerViewSet(viewsets.ModelViewSet):
    serializer_class = TallerSerializer
    queryset = _taller_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ClaseTallerViewSet(viewsets.ModelViewSet):
    serializer_class = ClaseTallerSerializer
    queryset = _clasetaller_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadSerializer
    queryset = _actividad_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ActividadRealizadaViewSet(viewsets.ModelViewSet):
    serializer_class = ActividadRealizadaSerializer
    queryset = _actividadrealizada_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class AsistenciaTallerViewSet(viewsets.ModelViewSet):
    serializer_class = AsistenciaTallerSerializer
    queryset = _asistenciataller_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ComportamientoViewSet(viewsets.ModelViewSet):
    serializer_class = ComportamientoSerializer
    queryset = _comportamiento_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class FactorClaseViewSet(viewsets.ModelViewSet):
    serializer_class = FactorClaseSerializer
    queryset = _factorclase_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class FactorGlobalViewSet(viewsets.ModelViewSet):
    serializer_class = FactorGlobalSerializer
    queryset = _factorglobal_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class UnidadObservacionViewSet(viewsets.ModelViewSet):
    serializer_class = UnidadObservacionSerializer
    queryset = _unidadobservacion_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class VariableUOViewSet(viewsets.ModelViewSet):
    serializer_class = VariableUOSerializer
    queryset = _variableuo_service.listar()
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(tags=['talleres']),
    retrieve=extend_schema(tags=['talleres']),
    create=extend_schema(tags=['talleres']),
    update=extend_schema(tags=['talleres']),
    partial_update=extend_schema(tags=['talleres']),
    destroy=extend_schema(tags=['talleres']),
)
class ValorVariableUOViewSet(viewsets.ModelViewSet):
    serializer_class = ValorVariableUOSerializer
    queryset = _valorvariableuo_service.listar()
    permission_classes = [IsAuthenticated]
