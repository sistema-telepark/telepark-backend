from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import Diagnostico, Direccion, Enfermedad, Evento, Localidad, Municipio, Persona, PersonaEp, Tipoevento, Tipoparentesco
from .serializers import DiagnosticoSerializer, DireccionSerializer, EnfermedadSerializer, EventoSerializer, LocalidadSerializer, MunicipioSerializer, PersonaEpSerializer, PersonaSerializer, TipoEventoSerializer, TipoparentescoSerializer

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

class EnfermedadViewSet(viewsets.ModelViewSet):
    serializer_class = EnfermedadSerializer
    queryset = Enfermedad.objects.all()
    permission_classes = [IsAuthenticated]

class DiagnosticoViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosticoSerializer
    queryset = Diagnostico.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_diagnosticoP(self, request, pk):
        diagnostico = Diagnostico.objects.filter(idpersonaep=pk)
        if request.method == 'GET': 
            diagnostico_serializer = DiagnosticoSerializer(diagnostico, many=True) 
            return JsonResponse(diagnostico_serializer.data, safe=False) 