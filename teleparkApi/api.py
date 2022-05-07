from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import action
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from .models import Evolucion, Diagnostico, Direccion, Enfermedad, Obrasocial, Os, Indicacionmedicamento, Medicamento, Evento, Localidad, Municipio, Persona, PersonaEp, Tipoevento, Tipoparentesco
from .serializers import EvolucionSerializer, DiagnosticoEpSerializer, DiagnosticoSerializer, DireccionSerializer, MedicamentoSerializer, IndicacionEpSerializer, IndicacionSerializer, EnfermedadSerializer, ObraSocialSerializer, OSEpSerializer, OSSerializer, EventoSerializer, LocalidadSerializer, MunicipioSerializer, PersonaEpSerializer, PersonaSerializer, PersonaPSerializer, TipoEventoSerializer, TipoparentescoSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()
    permission_classes = [IsAuthenticated]

class PersonaEPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaEpSerializer
    queryset = PersonaEp.objects.all()
    permission_classes = [IsAuthenticated]

class PersonaPViewSet(viewsets.ModelViewSet):
    serializer_class = PersonaPSerializer
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
            diagnostico_serializer = DiagnosticoEpSerializer(diagnostico, many=True) 
            return JsonResponse(diagnostico_serializer.data, safe=False)

class EvolucionViewSet(viewsets.ModelViewSet):
    serializer_class = EvolucionSerializer
    queryset = Evolucion.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_evolucionP(self, request, pk):
        evolucion = Evolucion.objects.filter(idpersonaep=pk)
        if request.method == 'GET': 
            evolucion_serializer = EvolucionSerializer(evolucion, many=True) 
            return JsonResponse(evolucion_serializer.data, safe=False)

class ObraSocialViewSet(viewsets.ModelViewSet):
    serializer_class = ObraSocialSerializer
    queryset = Obrasocial.objects.all()
    permission_classes = [IsAuthenticated]

class OSViewSet(viewsets.ModelViewSet):
    serializer_class = OSSerializer
    queryset = Os.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_obrasocialP(self, request, pk):
        obrasocial = Os.objects.filter(idpersonaep=pk)
        if request.method == 'GET': 
            obrasocial_serializer = OSEpSerializer(obrasocial, many=True) 
            return JsonResponse(obrasocial_serializer.data, safe=False)

class MedicamentoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    queryset = Medicamento.objects.all()
    permission_classes = [IsAuthenticated]

class IndicacionViewSet(viewsets.ModelViewSet):
    serializer_class = IndicacionSerializer
    queryset = Indicacionmedicamento.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_indicacionP(self, request, pk):
        indicacion = Indicacionmedicamento.objects.filter(idpersonaep=pk)
        if request.method == 'GET': 
            indicacion_serializer = IndicacionEpSerializer(indicacion, many=True) 
            return JsonResponse(indicacion_serializer.data, safe=False)