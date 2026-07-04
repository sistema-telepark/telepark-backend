from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    DireccionSerializer, LocalidadSerializer,
    MunicipioSerializer, PersonaEpSerializer,
    PersonaSerializer, PersonaPSerializer, TipoparentescoSerializer,
)
from .services import (
    PersonaService, PersonaEpService, DireccionService,
    TipoParentescoService, LocalidadService, MunicipioService,
)


_persona_service = PersonaService()
_personaep_service = PersonaEpService()
_direccion_service = DireccionService()
_tipoparentesco_service = TipoParentescoService()
_localidad_service = LocalidadService()
_municipio_service = MunicipioService()


class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = _persona_service.listar()
    permission_classes = [IsAuthenticated]


class PersonaEPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaEpSerializer
    queryset = _personaep_service.listar()
    permission_classes = [IsAuthenticated]


class PersonaPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaPSerializer
    queryset = _personaep_service.listar()
    permission_classes = [IsAuthenticated]


class LocalidadViewSet(viewsets.ModelViewSet):
    serializer_class = LocalidadSerializer
    queryset = _localidad_service.listar()
    permission_classes = [IsAuthenticated]


class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    queryset = _direccion_service.listar()
    permission_classes = [IsAuthenticated]


class TipoParentescoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoparentescoSerializer
    queryset = _tipoparentesco_service.listar()
    permission_classes = [IsAuthenticated]


class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializer
    queryset = _municipio_service.listar()
    permission_classes = [IsAuthenticated]
