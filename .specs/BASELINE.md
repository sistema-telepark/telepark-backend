# BASELINE — Telepark Backend

> **Propósito:** Fotografía exacta del código fuente actual (post CICLO-20260702-001 y CICLO-20260702-002).
> **Fecha de captura:** 2026-07-03
> **Último commit:** `7e191f9` — "[CICLO-20260702-001] Estabilizacion de entorno completa - Fase 10: verificacion final"
> **Hash:** `7e191f9993edcb846ab87686d8d46005c6872852`

---

## 1. Estructura del Proyecto

```
telepark-backend/
├── .specs/
│   ├── ARQUITECTURA.md            (937 líneas) — Contrato Dockerización + managed
│   ├── BASELINE.md                ← este archivo
│   ├── CAMBIOS.md                 (147 líneas) — Registro de cambios post-ciclos
│   ├── ESTADO.md                  (43 líneas) — Estado del pipeline actual
│   ├── GLOBAL_RULES.md            (47 líneas) — INMUTABLE
│   ├── REQUERIMIENTOS.md          (—)
│   └── requirements-baseline.txt  (—)
├── BD/
│   └── schema.sql
├── telepark/                      (proyecto Django — configuración)
│   ├── __init__.py
│   ├── asgi.py                    (16 líneas)
│   ├── settings.py                (184 líneas)
│   ├── urls.py                    (22 líneas)
│   └── wsgi.py                    (16 líneas)
├── teleparkApi/                   (aplicación Django única)
│   ├── migrations/
│   │   ├── 0001_initial.py        (340 líneas) — migración regenerada post-managed
│   │   └── __init__.py            (0 líneas)
│   ├── __init__.py
│   ├── api.py                     (121 líneas) — ViewSets (ARCHIVO CRÍTICO)
│   ├── apps.py                    (4 líneas)
│   ├── authentication.py          (93 líneas)
│   ├── handlers.py                (50 líneas) — NO USADO (dead code)
│   ├── helpers.py                 (14 líneas)
│   ├── middleware.py              (13 líneas) — NO EFECTIVO (dead code)
│   ├── models.py                  (275 líneas) — 26 modelos managed=True
│   ├── permission.py              (7 líneas)
│   ├── serializers.py             (146 líneas)
│   ├── static.py                  (5 líneas)
│   ├── urls.py                    (42 líneas)
│   └── views/
│       ├── __init__.py            (0 líneas)
│       └── health.py              (46 líneas) — Healthcheck endpoint
├── .dockerignore
├── Dockerfile                     (43 líneas)
├── docker-compose.yml             (56 líneas)
├── entrypoint.sh                  (66 líneas)
├── example.env                    (10 líneas)
├── manage.py                      (22 líneas)
└── requirements.txt               (14 paquetes)
```

**Archivos ELIMINADOS (ciclos anteriores):** `admin.py`, `tests.py`, `views.py`

**Total líneas Python (.py, excluyendo `__pycache__` y `.specs/`):** ~1.416 líneas

---

## 2. Dependencias Actuales (requirements.txt)

| Paquete | Versión | Estado | Recomendación |
|---------|---------|--------|---------------|
| Django | 6.0.6 | 🟢 Actualizado | LTS ideal sería 5.2, pero 6.0.6 es compatible |
| djangorestframework | 3.17.1 | 🟢 Actualizado | — |
| djangorestframework-simplejwt | 5.4.0 | 🟢 Actualizado | — |
| django-cors-headers | 4.6.0 | 🟢 Actualizado | — |
| mysqlclient | 2.2.7 | 🟢 Estable | — |
| python-dotenv | 1.0.1 | 🟢 Actualizado | — |
| PyJWT | 2.10.1 | 🟢 Actualizado | — |
| cryptography | 44.0.0 | 🟢 Actualizado | — |
| cffi | 1.17.1 | 🟢 Actualizado | Transitiva de cryptography |
| pycparser | 2.22 | 🟢 Actualizado | Transitiva de cffi |
| asgiref | 3.8.1 | 🟢 Actualizado | — |
| sqlparse | 0.5.3 | 🟢 Actualizado | — |
| typing_extensions | 4.12.2 | 🟢 Actualizado | — |
| tzdata | 2024.2 | 🟢 Actualizado | — |
| pytz | **ELIMINADO** | ✅ Eliminado | Reemplazado por zoneinfo stdlib |

**Dependencias funcionales directas:** Django, djangorestframework, django-cors-headers, djangorestframework-simplejwt, mysqlclient, python-dotenv, cryptography
**Paquetes ELIMINADOS (ciclo anterior):** django-rest-swagger, coreapi, coreschema, openapi-codec, uritemplate, itypes, requests, urllib3, certifi, Jinja2, simplejson, MarkupSafe, idna, charset-normalizer, setuptools, pytz

---

## 3. Endpoints Activos

### Endpoints directos:
| Método | Ruta | Función | Autenticación |
|--------|------|---------|---------------|
| POST | `/api/login` | `auth_view` | Pública |
| POST | `/api/create_user` | `create_user` | IsSuperuser |
| POST | `/api/refresh_token` | `TokenRefreshView` | Pública |
| GET | `/api/users` | `get_users` | IsSuperuser |
| PUT | `/api/update_user` | `update_user` | IsSuperuser |
| GET | `/api/health` | `health_check` | Pública 🆕 |

### Endpoints registrados vía DefaultRouter (ViewSets):
| ViewSet | Rutas generadas | Modelo |
|---------|-----------------|--------|
| PersonaViewSet | GET/POST `/api/persona`, GET/PUT/DELETE `/api/persona/{pk}` | Persona |
| PersonaEPViewSet | GET/POST `/api/personaEp`, GET/PUT/DELETE `/api/personaEp/{pk}` | PersonaEp |
| PersonaPViewSet | GET/POST `/api/personaP`, GET/PUT/DELETE `/api/personaP/{pk}` | PersonaEp 🔴 |
| DireccionViewSet | GET/POST `/api/direccion`, GET/PUT/DELETE `/api/direccion/{pk}` | Direccion |
| TipoParentescoViewSet | GET/POST `/api/tipoparentesco`, GET/PUT/DELETE `/api/tipoparentesco/{pk}` | Tipoparentesco |
| LocalidadViewSet | GET/POST `/api/localidad`, GET/PUT/DELETE `/api/localidad/{pk}` | Localidad |
| MunicipioViewSet | GET/POST `/api/municipio`, GET/PUT/DELETE `/api/municipio/{pk}` | Municipio |
| EventoViewSet | GET/POST `/api/evento`, GET/PUT/DELETE `/api/evento/{pk}` | Evento |
| TipoEventoViewSet | GET/POST `/api/tipoevento`, GET/PUT/DELETE `/api/tipoevento/{pk}` | Tipoevento |
| EnfermedadViewSet | GET/POST `/api/enfermedad`, GET/PUT/DELETE `/api/enfermedad/{pk}` | Enfermedad |
| DiagnosticoViewSet | GET/POST `/api/diagnostico`, GET/PUT/DELETE `/api/diagnostico/{pk}` + `GET /api/diagnostico/{pk}/personaep` | Diagnostico |
| EvolucionViewSet | GET/POST `/api/evolucion`, GET/PUT/DELETE `/api/evolucion/{pk}` + `GET /api/evolucion/{pk}/personaep` | Evolucion |
| ObraSocialViewSet | GET/POST `/api/obrasocial`, GET/PUT/DELETE `/api/obrasocial/{pk}` | Obrasocial |
| OSViewSet | GET/POST `/api/os`, GET/PUT/DELETE `/api/os/{pk}` + `GET /api/os/{pk}/personaep` | Os |
| MedicamentoViewSet | GET/POST `/api/medicamento`, GET/PUT/DELETE `/api/medicamento/{pk}` | Medicamento |
| IndicacionViewSet | GET/POST `/api/indicacion`, GET/PUT/DELETE `/api/indicacion/{pk}` + `GET /api/indicacion/{pk}/personaep` | Indicacionmedicamento |

### Acciones personalizadas (@action) con lógica de negocio:
| ViewSet | Acción | Ruta | Lógica |
|---------|--------|------|--------|
| DiagnosticoViewSet | `list_diagnosticoP` | `GET /api/diagnostico/{pk}/personaep` | Filtra Diagnostico por `idpersonaep=pk`, serializa con DiagnosticoEpSerializer |
| EvolucionViewSet | `list_evolucionP` | `GET /api/evolucion/{pk}/personaep` | Filtra Evolucion por `idpersonaep=pk`, serializa con EvolucionSerializer |
| OSViewSet | `list_obrasocialP` | `GET /api/os/{pk}/personaep` | Filtra Os por `idpersonaep=pk`, serializa con OSEpSerializer |
| IndicacionViewSet | `list_indicacionP` | `GET /api/indicacion/{pk}/personaep` | Filtra Indicacionmedicamento por `idpersonaep=pk`, serializa con IndicacionEpSerializer |

**Total endpoints activos: ~80+**

---

## 4. Serializadores

| Serializador | Modelo | Campos | Notas |
|-------------|--------|--------|-------|
| EvolucionSerializer | Evolucion | idevolucion, escalaevolucion, fecha, idpersonaep, borrado | Plano |
| EnfermedadSerializer | Enfermedad | idenfermedad, nombre | Plano |
| DiagnosticoEpSerializer | Diagnostico | iddiagnostico, fecha, idpersonaep, idenfermedad (anidado), borrado | Nested EnfermedadSerializer |
| DiagnosticoSerializer | Diagnostico | iddiagnostico, fecha, idpersonaep, idenfermedad, borrado | Plano (FK directa) |
| DireccionSerializer | Direccion | iddireccion, calle, departamento, numero, piso, idlocalidad | Plano |
| PersonaSerializer | Persona | idpersona, nombre, apellido, telefono, iddireccion, borrado, espaciente | Plano |
| PersonaEpSerializer | PersonaEp | activataller, escolaridadcompleta, fechainicio, fechanacimiento, maximaescolaridadalcanzada, sexo, tieneacompanante, tienecuidador, vivesolo, ocupacionprevia, ocupacionactual, idpersona, idreferente | Plano |
| PersonaPSerializer | PersonaEp | sexo, idpersona (anidado PersonaSerializer) | Nested — vista reducida |
| LocalidadSerializer | Localidad | idlocalidad, nombre, codigopostal, idmunicipio | Plano |
| MunicipioSerializer | Municipio | idmunicipio, nombre, provincia | Plano |
| TipoparentescoSerializer | Tipoparentesco | idpersona, idpersonaep, nombre | Plano |
| TipoEventoSerializer | Tipoevento | idtipoevento, nombre, desactivataller, borrado | Plano |
| EventoSerializer | Evento | idevento, fechadesde, fechahasta, motivo, idpersonaep, idtipoevento, borrado | 🔴 B002: `tipoEvento = TipoEventoSerializer` (class) |
| ObraSocialSerializer | Obrasocial | idobrasocial, nombre, esestatal | Plano |
| OSEpSerializer | Os | idos, idpersonaep, idobrasocial (anidado), borrado | Nested ObraSocialSerializer |
| OSSerializer | Os | idos, idpersonaep, idobrasocial, borrado | Plano |
| MedicamentoSerializer | Medicamento | idmedicamento, nombre, esantiparkinsoniano, eslevodopa | Plano |
| IndicacionEpSerializer | Indicacionmedicamento | idindicacion, cantidadmiligramos, estavigente, fechaprescripcion, horadetoma, idpersonaep, idmedicamento (anidado), borrado | Nested MedicamentoSerializer |
| IndicacionSerializer | Indicacionmedicamento | idindicacion, cantidadmiligramos, estavigente, fechaprescripcion, horadetoma, idpersonaep, idmedicamento, borrado | Plano |

---

## 5. Hallazgos

### 5.1. Código Muerto (Dead Code)

| ID | Archivo | Descripción |
|----|---------|-------------|
| D001 | `teleparkApi/handlers.py` (50 líneas) | **100% muerto.** Define `ICRUDStrategy`, `PostStrategy`, `GetStrategy`, `OtherStrategy`, `CRUDHandlerStrategies`. No es importado ni usado por ningún archivo del proyecto. Quedó relicto de una arquitectura anterior. |
| D002 | `teleparkApi/helpers.py:has_permission` (líneas 8-14) | El decorador `has_permission` no es importado ni usado por ningún archivo. |
| D003 | `teleparkApi/middleware.py` (13 líneas) | `ExceptionMiddleware.process_exception` **nunca es llamado por Django**. El método `process_exception` solo funciona con middleware antiguo (MiddlewareMixin). El middleware moderno (basado en `__call__`) no ejecuta `process_exception`. El error 500 queda manejado por defecto de Django. |

### 5.2. Bugs Activos

| ID | Archivo:Línea | Severidad | Descripción |
|----|--------------|-----------|-------------|
| B001 | `teleparkApi/api.py:24` | 🟡 Medio | **PersonaPViewSet usa queryset incorrecto:** `queryset = PersonaEp.objects.all()`. El ViewSet se llama `PersonaP` pero consulta el modelo `PersonaEp`. Debería tener su propio queryset o explicitar que es una vista alternativa de PersonaEp. |
| B002 | `teleparkApi/serializers.py:95` | 🟡 Medio | **EventoSerializer.tipoEvento es clase, no instancia:** `tipoEvento = TipoEventoSerializer` (asignación de clase, no instancia con `many=False, read_only=True`). El campo no serializa nested object. No se usa en `fields`. |
| B003 | `teleparkApi/api.py:70-71, 83-84, 101-102, 119-120` | 🟢 Bajo | **Redundancia de método en @action:** Todos los @action usan `methods=['get']` pero dentro del handler verifican `if request.method == 'GET'`. El chequeo es siempre verdadero e innecesario. |
| B004 | `teleparkApi/authentication.py:42-43, 62-63, 86-87` | 🟢 Bajo | **Doble verificación de permiso:** Las funciones usan `@permission_classes([IsSuperuser])` Y luego verifican manualmente `if(not request.user.is_superuser)`. El decorador ya asegura esto. |

### 5.3. Deuda Técnica — Violaciones de Arquitectura (GLOBAL_RULES.md)

| ID | Archivo | Violación |
|----|---------|-----------|
| **A001** | `teleparkApi/api.py` (todo el archivo) | **🔴 CRÍTICO — Lógica de negocio en capa de presentación.** Los ViewSets contienen consultas ORM directas (business logic) en los métodos `@action`. GLOBAL_RULES.md sección 1 establece: "Capa de Presentación: PROHIBIDO contener lógica de negocio". |
| A002 | `teleparkApi/api.py:12-121` | **🟡 Acoplamiento alto.** Todos los ViewSets heredan directamente de `viewsets.ModelViewSet` sin capa de servicio intermedia. No existe un directorio `services/`. |
| A003 | `teleparkApi/authentication.py` | **🟡 Lógica de negocio en vistas.** `auth_view`, `create_user`, `update_user`, `get_users` mezclan HTTP handling con lógica de dominio (validación, consultas, creación de usuarios). |
| A004 | General | **🟡 Ausencia de capa Services.** El proyecto no tiene carpeta `services/` ni clases service. Toda la lógica de negocio vive en api.py y authentication.py. |

### 5.4. Problemas de Seguridad

| ID | Aspecto | Estado | Detalle |
|----|---------|--------|---------|
| S001 | SECRET_KEY | 🟢 Resuelto | Migrado a variable de entorno |
| S002 | ALLOWED_HOSTS | 🟢 Resuelto | Migrado a variable de entorno |
| S003 | DEBUG | 🟢 Aceptable | `os.getenv("ENV") == 'dev'` |
| S004 | CSRF_TRUSTED_ORIGINS | 🟡 Mejorable | Desde env pero sin fallback en settings.py |
| S005 | JWT blacklist | 🟡 Ausente | `BLACKLIST_AFTER_ROTATION: False` — tokens refresh no invalidan anteriores |
| S006 | TLS no configurado | 🟡 Pendiente | Depende del proxy |
| S007 | Versión Django 6.0.6 | 🟢 Segura | Versión reciente con soporte activo |

### 5.5. handlers.py — Análisis de Relación con api.py

`CRUDHandlerStrategies` en `handlers.py` define un patrón Strategy con:
- `GetStrategy`: Ejecuta `Model.objects.all()` y serializa con `JsonResponse`
- `PostStrategy`: Parsea JSON, valida con serializer, guarda y responde 201/400
- `OtherStrategy`: Retorna 404

**Ninguno de los ViewSets en api.py usa `CRUDHandlerStrategies`.** Los ViewSets heredan de `ModelViewSet` que ya implementa CRUD por defecto. handlers.py es completamente código muerto.

---

## 6. Firma de Configuración

| Aspecto | Valor |
|---------|-------|
| Python | 3.14.2 |
| Django | 6.0.6 |
| DRF | 3.17.1 |
| simplejwt | 5.4.0 |
| Base de datos | MySQL 8.0 (vía mysqlclient 2.2.7) |
| Migraciones | 0001_initial.py (regenerada post-managed) |
| Modelos | 26 de negocio (managed=True) |
| Docker | Dockerfile + docker-compose.yml + entrypoint.sh |
| Autenticación | JWT (Bearer) via rest_framework_simplejwt |
| CORS | django-cors-headers 4.6.0 |
| Middleware | 8 estándar + ExceptionMiddleware (no efectivo) |

---

## 7. Arquitectura Objetivo para Próximo Ciclo

Basado en ESTADO.md y GLOBAL_RULES.md, el próximo ciclo debe:

1. **Extraer lógica de negocio de api.py** hacia servicios puros (`services/`)
2. **Migrar api.py → views.py** (convención Django estándar)
3. **Eliminar código muerto:** handlers.py, middleware.py (o corregirlo)
4. **Corregir bugs:** B001 (PersonaP queryset), B002 (EventoSerializer), B003 (redundancia @action), B004 (doble permiso)
5. **Implementar capa Services** con arquitectura: `views.py → services.py → models.py`
