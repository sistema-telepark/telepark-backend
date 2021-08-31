from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Direccion, Evento, Localidad, Municipio, Persona, PersonaEp, Tipoevento, Tipoparentesco
from .serializers import DireccionSerializer, EventoSerializer, LocalidadSerializer, MunicipioSerializer, PersonaEpSerializer, PersonaSerializer, TipoEventoSerializer, TipoparentescoSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()
    permission_classes = [IsAuthenticated]

class PersonaEPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaEpSerializer
    queryset = PersonaEp.objects.all()
    permission_classes = [IsAuthenticated]

class LocalidadViewSet(viewsets.ModelViewSet):
    serializer_class = LocalidadSerializer
    queryset = Localidad.objects.all()
    permission_classes = [IsAuthenticated]

class DireccionViewSet(viewsets.ModelViewSet):
    serializer_class = DireccionSerializer
    queryset = Direccion.objects.all()
    permission_classes = [IsAuthenticated]

class TipoParentescoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoparentescoSerializer
    queryset = Tipoparentesco.objects.all()
    permission_classes = [IsAuthenticated]

class MunicipioViewSet(viewsets.ModelViewSet):
    serializer_class = MunicipioSerializer
    queryset = Municipio.objects.all()
    permission_classes = [IsAuthenticated]

class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()
    permission_classes = [IsAuthenticated]

class TipoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoEventoSerializer
    queryset = Tipoevento.objects.all()
    permission_classes = [IsAuthenticated]