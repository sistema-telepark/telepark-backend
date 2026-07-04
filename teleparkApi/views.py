from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.db import connections, DEFAULT_DB_ALIAS
from django.db.utils import OperationalError
from django.http import JsonResponse

from .serializers import (
    EvolucionSerializer, DiagnosticoEpSerializer, DiagnosticoSerializer,
    DireccionSerializer, MedicamentoSerializer, IndicacionEpSerializer,
    IndicacionSerializer, EnfermedadSerializer, ObraSocialSerializer,
    OSEpSerializer, OSSerializer, EventoSerializer, LocalidadSerializer,
    MunicipioSerializer, PersonaEpSerializer, PersonaSerializer,
    PersonaPSerializer, TipoEventoSerializer, TipoparentescoSerializer,
)
from .services import (
    PersonaService, PersonaEpService, DireccionService,
    TipoParentescoService, LocalidadService, MunicipioService,
    DiagnosticoService, EvolucionService,
    ObraSocialService, OsService, IndicacionService,
    MedicamentoService, EventoService, TipoEventoService,
    EnfermedadService,
)


def health_check(request):
    result = {
        "status": "ok",
        "database": "unknown",
        "detail": None,
    }
    try:
        db_conn = connections[DEFAULT_DB_ALIAS]
        db_conn.ensure_connection()
        all_tables = db_conn.introspection.table_names()
        business_tables = [
            t for t in all_tables
            if not t.startswith('auth_') and not t.startswith('django_')
        ]
        result["database"] = "connected"
        result["tables"] = len(business_tables)
        return JsonResponse(result, status=200)
    except OperationalError:
        result["status"] = "error"
        result["database"] = "disconnected"
        result["detail"] = "Database connection failed"
        return JsonResponse(result, status=503)
    except Exception:
        result["status"] = "error"
        result["database"] = "disconnected"
        result["detail"] = "Health check failed"
        return JsonResponse(result, status=503)


_persona_service = PersonaService()
_personaep_service = PersonaEpService()
_direccion_service = DireccionService()
_tipoparentesco_service = TipoParentescoService()
_localidad_service = LocalidadService()
_municipio_service = MunicipioService()
_diagnostico_service = DiagnosticoService()
_evolucion_service = EvolucionService()
_obrasocial_service = ObraSocialService()
_os_service = OsService()
_medicamento_service = MedicamentoService()
_indicacion_service = IndicacionService()
_evento_service = EventoService()
_tipoevento_service = TipoEventoService()
_enfermedad_service = EnfermedadService()


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


class EventoViewSet(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = _evento_service.listar()
    permission_classes = [IsAuthenticated]


class TipoEventoViewSet(viewsets.ModelViewSet):
    serializer_class = TipoEventoSerializer
    queryset = _tipoevento_service.listar()
    permission_classes = [IsAuthenticated]


class EnfermedadViewSet(viewsets.ModelViewSet):
    serializer_class = EnfermedadSerializer
    queryset = _enfermedad_service.listar()
    permission_classes = [IsAuthenticated]


class DiagnosticoViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosticoSerializer
    queryset = _diagnostico_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_diagnosticoP(self, request, pk):
        diagnosticos = _diagnostico_service.filtrar_por_persona(pk)
        serializer = DiagnosticoEpSerializer(diagnosticos, many=True)
        return Response(serializer.data)


class EvolucionViewSet(viewsets.ModelViewSet):
    serializer_class = EvolucionSerializer
    queryset = _evolucion_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_evolucionP(self, request, pk):
        evoluciones = _evolucion_service.filtrar_por_persona(pk)
        serializer = EvolucionSerializer(evoluciones, many=True)
        return Response(serializer.data)


class ObraSocialViewSet(viewsets.ModelViewSet):
    serializer_class = ObraSocialSerializer
    queryset = _obrasocial_service.listar()
    permission_classes = [IsAuthenticated]


class OSViewSet(viewsets.ModelViewSet):
    serializer_class = OSSerializer
    queryset = _os_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_obrasocialP(self, request, pk):
        obrasociales = _os_service.filtrar_por_persona(pk)
        serializer = OSEpSerializer(obrasociales, many=True)
        return Response(serializer.data)


class MedicamentoViewSet(viewsets.ModelViewSet):
    serializer_class = MedicamentoSerializer
    queryset = _medicamento_service.listar()
    permission_classes = [IsAuthenticated]


class IndicacionViewSet(viewsets.ModelViewSet):
    serializer_class = IndicacionSerializer
    queryset = _indicacion_service.listar()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated],
            url_path='personaep', url_name='personaep')
    def list_indicacionP(self, request, pk):
        indicaciones = _indicacion_service.filtrar_por_persona(pk)
        serializer = IndicacionEpSerializer(indicaciones, many=True)
        return Response(serializer.data)
