from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.mixins import ModelPKMixin, NoPaginationMixin, auto_tag_schema_view

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


@auto_tag_schema_view
class TallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _taller_service
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ClaseTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _clasetaller_service
    serializer_class = ClaseTallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ActividadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _actividad_service
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ActividadRealizadaViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _actividadrealizada_service
    serializer_class = ActividadRealizadaSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class AsistenciaTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _asistenciataller_service
    serializer_class = AsistenciaTallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ComportamientoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _comportamiento_service
    serializer_class = ComportamientoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class FactorClaseViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _factorclase_service
    serializer_class = FactorClaseSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class FactorGlobalViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _factorglobal_service
    serializer_class = FactorGlobalSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class UnidadObservacionViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _unidadobservacion_service
    serializer_class = UnidadObservacionSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class VariableUOViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _variableuo_service
    serializer_class = VariableUOSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ValorVariableUOViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    service = _valorvariableuo_service
    serializer_class = ValorVariableUOSerializer
    permission_classes = [IsAuthenticated]
