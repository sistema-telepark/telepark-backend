# REQUERIMIENTOS — CICLO-20260704-001

## Modo
`BROWNFIELD`

## Contexto
El proyecto Telepark backend ha sido reestructurado exitosamente en 6 módulos Django (core, personas, salud, eventos, obra_social, talleres) con 27 ViewSets que exponen endpoints REST bajo el prefijo `/api/`. No existe actualmente documentación automática de la API — los endpoints solo pueden descubrirse leyendo el código fuente o las rutas en `core/urls.py`.

En el ciclo anterior (CICLO-20260703-002) se eliminaron del proyecto las dependencias legacy `django-rest-swagger`, `coreapi`, `coreschema`, `openapi-codec`, `uritemplate` e `itypes` por estar obsoletas e incompatibles con Django 6.0 / DRF 3.17.

Este ciclo propone integrar **`drf-spectacular`**, el generador de esquemas OpenAPI 3.0 estándar para DRF, para exponer documentación viva, interactiva y precisa de todos los endpoints del sistema, manteniendo las direcciones intactas.

**Compatibilidad verificada:** `drf-spectacular` soporta Django 3.2–6.0 y DRF 3.12–3.17 ✅.

---

## User Stories

| ID | Rol | Quiero | Para |
|----|-----|--------|------|
| US-01 | Arquitecto | Integrar `drf-spectacular` como generador OpenAPI 3.0 en el proyecto | Que la documentación de la API se genere automáticamente desde los ViewSets, sin mantenimiento manual |
| US-02 | Desarrollador | Tener un endpoint `/api/schema/` que exponga el esquema OpenAPI 3.0 completo | Poder validar que todos los endpoints, serializadores y métodos están correctamente declarados |
| US-03 | Desarrollador | Tener una UI Swagger interactiva en `/api/schema/swagger-ui/` con JWT Bearer Auth preconfigurado | Poder explorar y probar todos los endpoints desde el navegador sin herramientas externas |
| US-04 | QA Engineer | Tener una vista ReDoc en `/api/schema/redoc/` para lectura limpia de la documentación | Verificar la completitud del contrato de la API contra los criterios EARS |
| US-05 | Security Engineer | Que la documentación en producción requiera autenticación o esté deshabilitada | Prevenir exposición de información interna de la API en entornos productivos |
| US-06 | Desarrollador | Que todos los endpoints existentes bajo `/api/` sigan funcionando idénticamente tras la integración | Garantizar cero regresiones — la documentación es aditiva |

---

## Criterios de Aceptación (EARS)

### Ubiquitous (comportamiento siempre activo)

| ID | Criterio |
|----|----------|
| REQ-01 | El sistema DEBE agregar `'drf_spectacular'` a `INSTALLED_APPS` en `telepark/settings.py` |
| REQ-02 | El sistema DEBE configurar `DEFAULT_SCHEMA_CLASS = 'drf_spectacular.openapi.AutoSchema'` en `REST_FRAMEWORK` de `settings.py` |
| REQ-03 | El sistema DEBE incorporar `drf-spectacular` en `requirements.txt` como dependencia del proyecto |
| REQ-04 | El sistema DEBE exponer `GET /api/schema/` que devuelva el esquema OpenAPI 3.0 en formato YAML (content-type `application/vnd.oai.openapi`) |
| REQ-05 | El sistema DEBE exponer una UI Swagger interactiva en `GET /api/schema/swagger-ui/` con capacidad de autenticación Bearer JWT |
| REQ-06 | El sistema DEBE exponer una vista ReDoc en `GET /api/schema/redoc/` para documentación legible |
| REQ-07 | El esquema OpenAPI DEBE reflejar todos los ViewSets registrados: personas (7), salud (5), eventos (2), obra_social (2), talleres (11), más los endpoints de auth (login, create_user, users, update_user, refresh_token) y health_check — total 27 ViewSets + 5 endpoints funcionales |
| REQ-08 | El esquema OpenAPI DEBE incluir el esquema de seguridad `BearerAuth` (JWT) para todos los endpoints protegidos por `IsAuthenticated` |
| REQ-09 | El endpoint `GET /api/health` DEBE aparecer en el esquema como público (sin requerir autenticación) |
| REQ-10 | Todas las rutas documentadas DEBEN preservar exactamente los paths actuales (`/api/persona`, `/api/diagnostico`, `/api/evento`, etc.) — sin cambios de ruta |
| REQ-11 | El sistema DEBE configurar metadata del schema: `TITLE`, `DESCRIPTION`, `VERSION`, `CONTACT` en `SPECTACULAR_SETTINGS` |

### Event-driven (respuesta a eventos)

| ID | Criterio |
|----|----------|
| REQ-12 | CUANDO se agregue un nuevo ViewSet a cualquier módulo, el sistema DEBE reflejarlo automáticamente en el esquema OpenAPI sin intervención manual adicional |
| REQ-13 | CUANDO se ejecute `python manage.py spectacular --file schema.yaml` tras la integración, el sistema DEBE generar un archivo YAML válido sin errores |
| REQ-14 | CUANDO se acceda a la UI Swagger en modo DEBUG (`ENV=dev`), el sistema DEBE mostrar la interfaz completa sin requerir autenticación adicional en la UI |

### State-driven (comportamiento condicional)

| ID | Criterio |
|----|----------|
| REQ-15 | MIENTRAS `DEBUG = True`, los endpoints de documentación (`/api/schema/`, `/api/schema/swagger-ui/`, `/api/schema/redoc/`) DEBEN ser accesibles sin autenticación |
| REQ-16 | MIENTRAS `DEBUG = False` (producción), los endpoints de documentación DEBEN requerir autenticación JWT (restringidos a usuarios con rol `superuser`) O estar deshabilitados — según decisión del Arquitecto |
| REQ-17 | MIENTRAS los endpoints utilicen `JWTAuthentication`, el botón "Authorize" en Swagger UI DEBE estar preconfigurado para el esquema `Bearer <token>` |

### Unwanted-behavior (manejo de errores)

| ID | Criterio |
|----|----------|
| REQ-18 | SI `python manage.py check` reporta errores después de agregar `drf-spectacular`, ENTONCES el ciclo DEBE rechazarse y reportar los errores específicos |
| REQ-19 | SI un ViewSet carece de serializador explícito o tiene campos no tipables, ENTONCES `drf-spectacular` DEBE degradar gracefulmente usando inferencia automática sin romper el schema |
| REQ-20 | SI la integración modifica o elimina algún endpoint existente, ENTONCES el ciclo DEBE rechazarse inmediatamente (GATEKEEPER de regresiones) |

### Optional-feature (características opcionales)

| ID | Criterio |
|----|----------|
| REQ-21 | DONDE existan `@action` endpoints personalizados (`/api/diagnostico/{pk}/personaep`, `/api/evolucion/{pk}/personaep`, `/api/os/{pk}/personaep`, `/api/indicacion/{pk}/personaep`), el sistema DEBE documentarlos con sus métodos HTTP, parámetros de ruta y respuestas correctas |
| REQ-22 | DONDE se requiera servir assets de Swagger UI sin depender de CDN externos, el sistema PUEDE usar `drf-spectacular-sidecar` como distribución local alternativa |
| REQ-23 | DONDE se requiera limitar los esquemas expuestos, el sistema PUEDE usar `SCHEMA_COERCE_METHOD_NAMES` para unificar nombres de operación |

---

## Stack Tecnológico Propuesto

| Componente | Versión | Nota |
|-----------|---------|-------|
| **drf-spectacular** | **==0.29.0** | Última versión estable (Nov 2025). Generador OpenAPI 3.0 — compatible con Django 6.0 y DRF 3.17 verificados vía readthedocs |
| **PyYAML** | ≥6.0 | Dependencia de drf-spectacular para serialización YAML |
| *drf-spectacular-sidecar* | *opcional* | Solo si se opta por REQ-22 (assets locales sin CDN) |

**Sin cambios al stack existente:** Python 3.14.2, Django 6.0.6, DRF 3.17.1, simplejwt 5.5.1.

---

## Trazabilidad US ↔ REQ

| User Story | Criterios EARS |
|------------|----------------|
| US-01 — Integrar drf-spectacular | REQ-01, REQ-02, REQ-03, REQ-11 |
| US-02 — Schema endpoint | REQ-04, REQ-13 |
| US-03 — Swagger UI | REQ-05, REQ-14, REQ-17 |
| US-04 — ReDoc | REQ-06 |
| US-05 — Seguridad en producción | REQ-15, REQ-16 |
| US-06 — Sin regresiones | REQ-07, REQ-08, REQ-09, REQ-10, REQ-18, REQ-20 |

---

## Mapa de Endpoints para documentar

| Ruta | ViewSet/Función | Módulo | Auth |
|------|----------------|--------|------|
| `GET /api/health` | `health_check` | core | ❌ Público |
| `POST /api/login` | `auth_view` | core | ❌ Público |
| `POST /api/create_user` | `create_user` | core | 🔒 IsSuperuser |
| `GET /api/users` | `get_users` | core | 🔒 IsSuperuser |
| `PUT /api/update_user` | `update_user` | core | 🔒 IsSuperuser |
| `POST /api/refresh_token` | `TokenRefreshView` | core | ❌ Público |
| `GET/POST/PUT/DELETE /api/persona` | PersonaViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/personaEp` | PersonaEPViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/personaP` | PersonaPViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/direccion` | DireccionViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/tipoparentesco` | TipoParentescoViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/localidad` | LocalidadViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/municipio` | MunicipioViewSet | personas | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/diagnostico` | DiagnosticoViewSet | salud | 🔒 IsAuthenticated |
| `GET /api/diagnostico/{pk}/personaep` | DiagnosticoViewSet @action | salud | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/evolucion` | EvolucionViewSet | salud | 🔒 IsAuthenticated |
| `GET /api/evolucion/{pk}/personaep` | EvolucionViewSet @action | salud | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/enfermedad` | EnfermedadViewSet | salud | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/medicamento` | MedicamentoViewSet | salud | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/indicacion` | IndicacionViewSet | salud | 🔒 IsAuthenticated |
| `GET /api/indicacion/{pk}/personaep` | IndicacionViewSet @action | salud | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/evento` | EventoViewSet | eventos | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/tipoevento` | TipoEventoViewSet | eventos | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/obrasocial` | ObraSocialViewSet | obra_social | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/os` | OSViewSet | obra_social | 🔒 IsAuthenticated |
| `GET /api/os/{pk}/personaep` | OSViewSet @action | obra_social | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/taller` | TallerViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/clasetaller` | ClaseTallerViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/actividad` | ActividadViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/actividadrealizada` | ActividadRealizadaViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/asistenciataller` | AsistenciaTallerViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/comportamiento` | ComportamientoViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/factorclase` | FactorClaseViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/factorglobal` | FactorGlobalViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/unidadobservacion` | UnidadObservacionViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/variableuo` | VariableUOViewSet | talleres | 🔒 IsAuthenticated |
| `GET/POST/PUT/DELETE /api/valorvariableuo` | ValorVariableUOViewSet | talleres | 🔒 IsAuthenticated |

---

## Fuera de Alcance

| Item | Justificación |
|------|---------------|
| Migrar a OpenAPI 2.0 (Swagger 2.0) | drf-spectacular genera OpenAPI 3.0, el estándar actual. No hay razón para usar Swagger 2.0 |
| Generar clientes de API automáticamente | Fuera del alcance de este ciclo — se centra solo en documentación y visualización |
| Autenticación OAuth2 en Swagger UI | El sistema usa JWT Bearer via simplejwt. OAuth2 no está en el stack actual |
| Agregar tests unitarios para la documentación | La documentación es un artefacto derivado del código — su verificación es visual y funcional |
| Refactorizar endpoints o agregar nuevos | Este ciclo es puramente aditivo — no modifica la API existente |
| Migrar de CDN a SIDECAR para assets | Se deja como opcional (REQ-22) para un ciclo futuro si es necesario |

---

## Checklist de Seguridad (GLOBAL_RULES.md)

| Regla Global | Aplicación en este ciclo |
|-------------|--------------------------|
| §2.2 Validación de entradas | El schema OpenAPI se genera desde serializadores existentes — no introduce nuevas superficies de validación |
| §2.3 IAM / JWT | El esquema de seguridad Bearer JWT se configura en `SPECTACULAR_SETTINGS.SECURITY_SCHEME` |
| §2.4 Protección de datos | Los esquemas no exponen datos sensibles — solo tipos, estructuras y constraints de serializadores |
| §2.5 Observabilidad / Logging | Los endpoints de documentación no logean requests ni exponen PII |
| §2.5 Manejo de errores | Errores de schema se traducen en warnings de `drf-spectacular`, no en stacktraces |
| §3 Checklist Revisor/QA | Endpoints de documentación deben tener auth explícita en producción (REQ-16) |

---

## Notas Técnicas

### Instalación esperada

```bash
pip install drf-spectacular==0.29.0
pip freeze | findstr drf-spectacular >> requirements.txt
```

### Configuración estimada en settings.py

```python
INSTALLED_APPS += ['drf_spectacular',]

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Telepark API',
    'DESCRIPTION': 'API REST del sistema Telepark — módulos: personas, salud, eventos, obra_social, talleres',
    'VERSION': '1.0.0',
    'CONTACT': {'email': 'admin@telepark.com'},
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SERVE_INCLUDE_SCHEMA': False,
    'SECURITY': [{'BearerAuth': []}],
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
}
```

### URLs estimadas en core/urls.py

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Al inicio o al final de urlpatterns:
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
```

### Verificación de integridad

```bash
python manage.py check                    # 0 errores
python manage.py spectacular --file schema.yaml   # archivo YAML generado sin errores
```
