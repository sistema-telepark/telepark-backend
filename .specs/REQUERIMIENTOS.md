# REQUERIMIENTOS — CICLO CICLO-20260703-001

## Modo
`BROWNFIELD`

## Contexto
El proyecto Telepark tiene una deuda técnica crítica de acoplamiento en la capa web identificada como **A001** en BASELINE.md: toda la lógica de negocio (consultas ORM, validaciones, reglas de dominio) reside dentro de los ViewSets en `teleparkApi/api.py`, violando la **Regla 1 de GLOBAL_RULES.md** que establece: *"Capa de Presentación: PROHIBIDO contener lógica de negocio"*.

Adicionalmente, el archivo se llama `api.py` cuando la convención Django estándar es `views.py` (el archivo `views.py` original fue eliminado en CICLO-20260702-001 por ser código muerto).

No existe una capa de Servicios (`services/`) que encapsule las reglas de negocio, dejando a los ViewSets como controladores monolíticos que mezclan responsabilidades HTTP con lógica de dominio.

Este ciclo busca:
1. **Crear la capa de Servicios** puros (`services/`) para encapsular toda la lógica de negocio
2. **Migrar `api.py` → `views.py`** siguiendo la convención Django estándar
3. **Refactorizar los ViewSets** para que sean únicamente adaptadores HTTP delgados
4. **Eliminar código muerto** identificado (handlers.py) que quedó relicto de una arquitectura previa

---

## User Stories

| ID | Rol | Quiero | Para |
|----|-----|--------|------|
| US-01 | Desarrollador | Que exista una capa de Servicios puros (`services/`) que encapsule toda la lógica de negocio (consultas ORM, validaciones, reglas de dominio) actualmente dispersa en los ViewSets | Separar responsabilidades y cumplir con la arquitectura de capas definida en GLOBAL_RULES.md |
| US-02 | Desarrollador | Que los ViewSets en `api.py` sean migrados a `views.py` y refactorizados como adaptadores HTTP delgados que solo reciban requests, deleguen en servicios y devuelvan responses | Tener una separación limpia entre la capa de presentación y la lógica de dominio |
| US-03 | Desarrollador | Que las 4 acciones personalizadas `@action` (Diagnostico.list_diagnosticoP, Evolucion.list_evolucionP, OS.list_obrasocialP, Indicacion.list_indicacionP) deleguen su lógica de filtrado a los Servicios en lugar de ejecutar ORM directamente en el ViewSet | Que todas las consultas a la base de datos estén centralizadas y reutilizables en la capa de Servicios |
| US-04 | Arquitecto | Que el archivo `handlers.py` (50 líneas, 100% código muerto) sea eliminado del proyecto | Eliminar código relicto que ya no cumple ninguna función y reduce la mantenibilidad |
| US-05 | QA Engineer | Poder verificar mediante pruebas que los endpoints existentes se comportan idénticamente antes y después de la refactorización (mismos datos de entrada producen mismas respuestas) | Asegurar que la extracción a Servicios no introduce regresiones funcionales |

---

## Criterios de Aceptación (EARS)

### Ubiquitous (comportamiento siempre activo)

| ID | Criterio |
|----|----------|
| REQ-01 | El sistema DEBE tener una carpeta `teleparkApi/services/` con un archivo `__init__.py` y módulos de servicio que encapsulen toda la lógica de negocio actualmente en los ViewSets |
| REQ-02 | El archivo `teleparkApi/api.py` DEBE ser renombrado/migrado a `teleparkApi/views.py` (convención Django estándar) |
| REQ-03 | Cada ViewSet en `views.py` DEBE delegar TODAS las operaciones de negocio (consultas ORM, validaciones, reglas de dominio) a la capa de Servicios |
| REQ-04 | Los ViewSets DEBEN limitarse a: recibir un `request`, invocar al Servicio correspondiente, y devolver una `Response` DRF |
| REQ-05 | El archivo `teleparkApi/handlers.py` DEBE ser eliminado del proyecto por ser código muerto (no importado ni usado por ningún archivo) |
| REQ-06 | La capa de Servicios DEBE usar los Modelos de Django directamente (sin pasar por serializadores), retornando datos procesados o resultados de operaciones |
| REQ-07 | Cada Servicio DEBE ser una clase Python pura (sin herencia de DRF) con métodos que representen operaciones de negocio (ej: `listar()`, `obtener_por_id()`, `filtrar_por_persona()`) |

### Event-driven (respuesta a eventos)

| ID | Criterio |
|----|----------|
| REQ-08 | CUANDO se realice una petición GET a `/api/diagnostico/{pk}/personaep`, el ViewSet `DiagnosticoViewSet` DEBE invocar un método del Servicio de Diagnóstico en lugar de ejecutar `Diagnostico.objects.filter(idpersonaep=pk)` directamente |
| REQ-09 | CUANDO se realice una petición GET a `/api/evolucion/{pk}/personaep`, el ViewSet `EvolucionViewSet` DEBE invocar un método del Servicio de Evolución |
| REQ-10 | CUANDO se realice una petición GET a `/api/os/{pk}/personaep`, el ViewSet `OSViewSet` DEBE invocar un método del Servicio de Obra Social |
| REQ-11 | CUANDO se realice una petición GET a `/api/indicacion/{pk}/personaep`, el ViewSet `IndicacionViewSet` DEBE invocar un método del Servicio de Indicación |
| REQ-12 | CUANDO se ejecute `python manage.py check` después de la refactorización, el sistema DEBE reportar 0 errores y 0 warnings (excluyendo warnings preexistentes de configuración) |
| REQ-13 | CUANDO se ejecute `python manage.py test`, el sistema DEBE ejecutar las pruebas sin errores de importación |

### State-driven (comportamiento condicional)

| ID | Criterio |
|----|----------|
| REQ-14 | MIENTRAS el ViewSet herede de `ModelViewSet`, DEBE sobrescribir los métodos `list()`, `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` para delegar en Servicios (o configurar `queryset` y `serializer_class` para casos CRUD puros sin lógica extra) |
| REQ-15 | MIENTRAS un Servicio realice consultas a la BD, DEBE usar el ORM de Django (prohibido raw SQL por seguridad, según GLOBAL_RULES.md sección 2.2) |

### Unwanted-behavior (manejo de errores)

| ID | Criterio |
|----|----------|
| REQ-16 | SI un Servicio encuentra un error de dominio (ej: registro no encontrado, violación de regla de negocio), ENTONCES DEBE lanzar una excepción de dominio personalizada que el ViewSet capture y convierta en una respuesta HTTP apropiada (404, 400, etc.) |
| REQ-17 | SI durante la refactorización se rompe algún endpoint existente, ENTONCES el ciclo DEBE rechazarse y reportar el error específico (sujeto al circuit breaker) |

### Optional-feature (características opcionales)

| ID | Criterio |
|----|----------|
| REQ-18 | DONDE exista la oportunidad de corregir bugs menores (B001: PersonaP queryset incorrecto, B002: EventoSerializer tipoEvento clase), el desarrollador PUEDE corregirlos como parte de la refactorización siempre que no aumente el alcance del ciclo |
| REQ-19 | DONDE se identifiquen dependencias o patrones comunes entre servicios, el desarrollador PUEDE crear un `BaseService` o clase abstracta para reducir duplicación |

---

## Trazabilidad US ↔ REQ

| User Story | Criterios EARS |
|------------|----------------|
| US-01 | REQ-01, REQ-06, REQ-07, REQ-15 |
| US-02 | REQ-02, REQ-03, REQ-04, REQ-14 |
| US-03 | REQ-08, REQ-09, REQ-10, REQ-11 |
| US-04 | REQ-05 |
| US-05 | REQ-12, REQ-13, REQ-16, REQ-17 |

---

## Trazabilidad REQ ↔ Hallazgos BASELINE.md

| Criterio EARS | Hallazgo asociado |
|---------------|-------------------|
| REQ-01, REQ-02, REQ-03, REQ-04, REQ-07, REQ-14 | **A001**, **A002**, **A004** — Lógica de negocio en ViewSets, acoplamiento, ausencia de servicios |
| REQ-05 | **D001** — handlers.py 100% código muerto |
| REQ-08, REQ-09, REQ-10, REQ-11 | **B003** — Acciones @action con lógica ORM inline |
| REQ-18 | **B001**, **B002** — Bugs opcionales a corregir |
| REQ-15 | GLOBAL_RULES.md 2.2 — Prohibición de raw SQL |

---

## Fuera de Alcance

| Item | Justificación |
|------|---------------|
| Corregir middleware.py (D003) | No afecta la funcionalidad actual y está fuera del objetivo de extracción a Servicios |
| Corregir B004 (doble verificación de permisos en authentication.py) | Es código de autenticación, no de ViewSets ni servicios |
| Agregar tests unitarios de servicios | Se prioriza la refactorización funcional; los tests se abordarán en ciclo posterior de QA |
| Dockerizar cambios o modificar Dockerfile | La Dockerización ya está completa en CICLO-20260702-002 |
| Actualizar Django, DRF o dependencias | Las dependencias ya fueron actualizadas en CICLO-20260702-001 |
| Renombrar o modificar modelos/serializadores existentes | Solo se modifica la capa de presentación y se crea la de servicios |
| Implementar autenticación adicional o autorización | Fuera del alcance de esta refactorización arquitectónica |
| Migrar a base de datos diferente a MySQL | No aplica |

---

## Notas Técnicas

- **Estructura objetivo de la capa Services:**
  ```
  teleparkApi/services/
  ├── __init__.py
  ├── base_service.py          (opcional - clase base)
  ├── persona_service.py       (servicios de Persona, PersonaEp)
  ├── diagnostico_service.py   (servicios de Diagnostico)
  ├── evolucion_service.py     (servicios de Evolucion)
  ├── os_service.py            (servicios de ObraSocial, Os)
  ├── indicacion_service.py    (servicios de Indicacionmedicamento)
  └── ... (demás servicios por dominio)
  ```

- **Migración api.py → views.py:**
  - Crear `teleparkApi/views/` (ya existe con `__init__.py` y `health.py`)
  - Mover contenido de `api.py` a `views/api_views.py` o directamente a `views.py`
  - Actualizar importaciones en `urls.py` y demás archivos referenciantes

- **Patrón de Servicio:**
  ```python
  class DiagnosticoService:
      def listar(self) -> QuerySet:
          return Diagnostico.objects.all()
      
      def obtener_por_id(self, pk: int) -> Diagnostico:
          return Diagnostico.objects.get(pk=pk)
      
      def filtrar_por_persona(self, personaep_pk: int) -> QuerySet:
          return Diagnostico.objects.filter(idpersonaep=personaep_pk)
  ```

- **ViewSets resultantes (adaptadores HTTP puros):**
  ```python
  class DiagnosticoViewSet(viewsets.ModelViewSet):
      queryset = DiagnosticoService().listar()
      serializer_class = DiagnosticoSerializer
      
      @action(detail=True, methods=['get'])
      def personaep(self, request, pk=None):
          diagnosticos = DiagnosticoService().filtrar_por_persona(pk)
          serializer = DiagnosticoEpSerializer(diagnosticos, many=True)
          return Response(serializer.data)
  ```
