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
from .models import (
    Taller, Clasetaller, Actividad, Actividadrealizada,
    Asistenciataller, Comportamiento, Factorclase, Factorglobal,
    Unidadobservacion, Variableuo, Valorvariableuo,
)


@auto_tag_schema_view
class TallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Taller.objects
    serializer_class = TallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ClaseTallerViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Clasetaller.objects
    serializer_class = ClaseTallerSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class ActividadViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Actividad.objects
    serializer_class = ActividadSerializer
    permission_classes = [IsAuthenticated]


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
class ComportamientoViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Comportamiento.objects
    serializer_class = ComportamientoSerializer
    permission_classes = [IsAuthenticated]


@auto_tag_schema_view
class FactorClaseViewSet(NoPaginationMixin, ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Factorclase.objects
    serializer_class = FactorClaseSerializer
    permission_classes = [IsAuthenticated]


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
class ValorVariableUOViewSet(ModelPKMixin, viewsets.ModelViewSet):
    app_tag = 'talleres'
    manager = Valorvariableuo.objects
    serializer_class = ValorVariableUOSerializer
    permission_classes = [IsAuthenticated]
