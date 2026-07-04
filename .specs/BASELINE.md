# BASELINE — Telepark Backend (REFRESHED)

> **Propósito:** Fotografía exacta del código fuente actual antes del ciclo de integración Swagger/OpenAPI.
> **Fecha de captura:** 2026-07-04
> **Último commit:** 6c8dafc — "refactor: dividir monolito teleparkApi en 6 modulos (core, personas, salud, eventos, obra_social, talleres)"
> **Hash:** 6c8dafcfb0c5520f27e6d77651d17431829430f7

---

## 1. Estructura del Proyecto

`
telepark-backend/
├── .specs/
│   ├── ARQUITECTURA.md            (—) — Contrato Dockerización + managed
│   ├── BASELINE.md                ← este archivo (REFRESHED)
│   ├── CAMBIOS.md                 (—) — Historial de ciclos anteriores
│   ├── ESTADO.md                  (—) — Ciclo CICLO-20260704-001 en REQUERIMIENTOS
│   ├── GLOBAL_RULES.md            (47 líneas) — INMUTABLE
│   ├── REQUERIMIENTOS.md          (—) — Requerimientos Swagger/OpenAPI
│   └── requirements-baseline.txt  (—)
├── BD/
│   ├── schema.sql
│   ├── SCRIPT_BD 19-04-2022.txt
│   └── pruebatelepark.mwb
├── core/                          (infraestructura compartida)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — CoreConfig
│   ├── authentication.py          (104 líneas) — auth_view, create_user, get_users, update_user
│   ├── helpers.py                 (14 líneas) — check_attributes, has_permission
│   ├── middleware.py              (12 líneas) — ExceptionMiddleware
│   ├── permission.py              (7 líneas)  — IsSuperuser
│   ├── static.py                  (5 líneas)  — HTTP_METHOD enum
│   ├── views.py                   (32 líneas) — health_check
│   ├── urls.py                    (21 líneas) — Router central: incluye auth + health + 5 módulos
│   └── migrations/
│       └── __init__.py
├── personas/                      (raíz del dominio — sin dependencias externas)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — PersonasConfig
│   ├── models.py                  (75 líneas) — 6 modelos
│   ├── serializers.py             (63 líneas) — 7 serializadores
│   ├── services.py                (64 líneas) — BaseService + 6 servicios
│   ├── views.py                   (62 líneas) — 7 ViewSets
│   ├── urls.py                    (18 líneas) — Router con 7 endpoints
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── salud/                         (→ personas)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — SaludConfig
│   ├── models.py                  (55 líneas) — 5 modelos
│   ├── serializers.py             (73 líneas) — 7 serializadores
│   ├── services.py                (69 líneas) — BaseService + 5 servicios
│   ├── views.py                   (73 líneas) — 5 ViewSets (+ @action)
│   ├── urls.py                    (15 líneas) — Router con 5 endpoints
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── eventos/                       (→ personas)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — EventosConfig
│   ├── models.py                  (24 líneas) — 2 modelos
│   ├── serializers.py             (16 líneas) — 2 serializadores
│   ├── services.py                (46 líneas) — BaseService + 2 servicios
│   ├── views.py                   (21 líneas) — 2 ViewSets
│   ├── urls.py                    (9 líneas)  — Router con 2 endpoints
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── obra_social/                   (→ personas)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — ObraSocialConfig
│   ├── models.py                  (20 líneas) — 2 modelos
│   ├── serializers.py             (22 líneas) — 3 serializadores
│   ├── services.py                (49 líneas) — BaseService + 2 servicios
│   ├── views.py                   (32 líneas) — 2 ViewSets (+ @action)
│   ├── urls.py                    (9 líneas)  — Router con 2 endpoints
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── talleres/                      (→ personas)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — TalleresConfig
│   ├── models.py                  (100 líneas) — 11 modelos
│   ├── serializers.py             (72 líneas) — 11 serializadores
│   ├── services.py                (86 líneas) — BaseService + 11 servicios
│   ├── views.py                   (96 líneas) — 11 ViewSets
│   ├── urls.py                    (24 líneas) — Router con 11 endpoints
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── telepark/                      (proyecto Django — configuración)
│   ├── __init__.py
│   ├── asgi.py                    (16 líneas)
│   ├── settings.py                (190 líneas) — 6 módulos en INSTALLED_APPS
│   ├── urls.py                    (22 líneas) — Incluye core.urls
│   └── wsgi.py                    (16 líneas)
├── Dockerfile                     (—)
├── docker-compose.yml             (—)
├── entrypoint.sh                  (—)
├── .dockerignore                  (—)
├── manage.py
├── requirements.txt
├── .env
├── example.env
├── .gitignore
├── README.md
├── AGENTS.md
└── package-lock.json
`

## 2. Modelos de Dominio (26 modelos distribuidos en 5 módulos)

### 2.1. Mapa de Entidades y Relaciones

`
Persona ──1:1── PersonaEp ──FK── Tipoparentesco
   │                    │
   │                    ├──FK── Diagnostico ──FK── Enfermedad
   │                    ├──FK── Evolucion
   │                    ├──FK── Evento ──FK── TipoEvento
   │                    ├──FK── Os ──FK── ObraSocial
   │                    ├──FK── Indicacionmedicamento ──FK── Medicamento
   │                    └──FK── Asistenciataller ──FK── Clasetaller ──FK── Taller
   │                                          └──FK── Comportamiento
   │                                                      └──FK── Variableuo ──FK── Unidadobservacion
   │                                                                  └──FK── Valorvariableuo
   │
   └──FK── Direccion ──FK── Localidad ──FK── Municipio

Taller ──FK── Actividad ──1:1── Actividadrealizada ──FK── Clasetaller
Clasetaller ──1:1── Factorclase ──FK── Factorglobal
`

### 2.2. Distribución por Módulo

| Módulo | Modelos | FK externas |
|--------|---------|-------------|
| **personas** (6) | Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco | Direccion→Localidad, Localidad→Municipio, PersonaEp→Persona, Tipoparentesco→Persona+PersonaEp |
| **salud** (5) | Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento | Diagnostico→personas.PersonaEp+Enfermedad, Evolucion→personas.PersonaEp, Indicacionmedicamento→personas.PersonaEp+Medicamento |
| **eventos** (2) | Evento, Tipoevento | Evento→personas.PersonaEp+Tipoevento |
| **obra_social** (2) | Obrasocial, Os | Os→personas.PersonaEp+Obrasocial |
| **talleres** (11) | Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo | Asistenciataller→personas.PersonaEp+Clasetaller+Comportamiento, Actividadrealizada→Actividad+Clasetaller, Factorclase→Clasetaller+Factorglobal, Variableuo→Comportamiento+Unidadobservacion, Valorvariableuo→Variableuo |

> **Nota:** Todas las FKs entre módulos usan string refs: models.ForeignKey('personas.PersonaEp', ...). DAG: personas ← {salud, eventos, obra_social, talleres}. Sin ciclos.

## 3. Capa de Servicios (26 clases, distribuidas en 5 módulos)

### 3.1. BaseService (duplicado en cada módulo)

Cada módulo de dominio define su propio BaseService con los métodos genéricos: listar(), obtener_por_id(), crear(), ctualizar(), eliminar(), además de ServiceException y NotFoundException.

### 3.2. Servicios por Módulo

| Módulo | Clase | Modelo | Métodos extra |
|--------|-------|--------|---------------|
| **personas** | PersonaService | Persona | — |
| | PersonaEpService | PersonaEp | — |
| | DireccionService | Direccion | — |
| | TipoParentescoService | Tipoparentesco | — |
| | LocalidadService | Localidad | — |
| | MunicipioService | Municipio | — |
| **salud** | DiagnosticoService | Diagnostico | iltrar_por_persona() |
| | EvolucionService | Evolucion | iltrar_por_persona() |
| | EnfermedadService | Enfermedad | — |
| | MedicamentoService | Medicamento | — |
| | IndicacionService | Indicacionmedicamento | iltrar_por_persona() |
| **eventos** | EventoService | Evento | — |
| | TipoEventoService | Tipoevento | — |
| **obra_social** | ObraSocialService | Obrasocial | — |
| | OsService | Os | iltrar_por_persona() |
| **talleres** | TallerService | Taller | — |
| | ClaseTallerService | Clasetaller | — |
| | ActividadService | Actividad | — |
| | ActividadRealizadaService | Actividadrealizada | — |
| | AsistenciaTallerService | Asistenciataller | — |
| | ComportamientoService | Comportamiento | — |
| | FactorClaseService | Factorclase | — |
| | FactorGlobalService | Factorglobal | — |
| | UnidadObservacionService | Unidadobservacion | — |
| | VariableUOService | Variableuo | — |
| | ValorVariableUOService | Valorvariableuo | — |

> **Nota:** Ahora todos los modelos (26/26) tienen servicios asociados. Ya no hay modelos sin capa de negocio.

## 4. Capa de Presentación (27 ViewSets en 5 módulos)

Todos heredan de ModelViewSet con IsAuthenticated.

### 4.1. Módulo personas (7 ViewSets)

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| PersonaViewSet | PersonaSerializer | PersonaService |
| PersonaEPViewSet | PersonaEpSerializer | PersonaEpService |
| PersonaPViewSet | PersonaPSerializer | PersonaEpService |
| LocalidadViewSet | LocalidadSerializer | LocalidadService |
| DireccionViewSet | DireccionSerializer | DireccionService |
| TipoParentescoViewSet | TipoparentescoSerializer | TipoParentescoService |
| MunicipioViewSet | MunicipioSerializer | MunicipioService |

### 4.2. Módulo salud (5 ViewSets)

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| DiagnosticoViewSet | DiagnosticoSerializer (+ @action) | DiagnosticoService |
| EvolucionViewSet | EvolucionSerializer (+ @action) | EvolucionService |
| EnfermedadViewSet | EnfermedadSerializer | EnfermedadService |
| MedicamentoViewSet | MedicamentoSerializer | MedicamentoService |
| IndicacionViewSet | IndicacionSerializer (+ @action) | IndicacionService |

### 4.3. Módulo eventos (2 ViewSets)

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| EventoViewSet | EventoSerializer | EventoService |
| TipoEventoViewSet | TipoEventoSerializer | TipoEventoService |

### 4.4. Módulo obra_social (2 ViewSets)

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| ObraSocialViewSet | ObraSocialSerializer | ObraSocialService |
| OSViewSet | OSSerializer (+ @action) | OsService |

### 4.5. Módulo talleres (11 ViewSets)

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| TallerViewSet | TallerSerializer | TallerService |
| ClaseTallerViewSet | ClaseTallerSerializer | ClaseTallerService |
| ActividadViewSet | ActividadSerializer | ActividadService |
| ActividadRealizadaViewSet | ActividadRealizadaSerializer | ActividadRealizadaService |
| AsistenciaTallerViewSet | AsistenciaTallerSerializer | AsistenciaTallerService |
| ComportamientoViewSet | ComportamientoSerializer | ComportamientoService |
| FactorClaseViewSet | FactorClaseSerializer | FactorClaseService |
| FactorGlobalViewSet | FactorGlobalSerializer | FactorGlobalService |
| UnidadObservacionViewSet | UnidadObservacionSerializer | UnidadObservacionService |
| VariableUOViewSet | VariableUOSerializer | VariableUOService |
| ValorVariableUOViewSet | ValorVariableUOSerializer | ValorVariableUOService |

### 4.6. @action endpoints (cross-context, preservados)

- DiagnosticoViewSet.list_diagnosticoP → GET /api/diagnostico/{pk}/personaep
- EvolucionViewSet.list_evolucionP → GET /api/evolucion/{pk}/personaep
- OSViewSet.list_obrasocialP → GET /api/os/{pk}/personaep
- IndicacionViewSet.list_indicacionP → GET /api/indicacion/{pk}/personaep

## 5. Serializadores (30 serializadores distribuidos en 5 módulos)

### 5.1. Módulo personas (7 serializadores)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| PersonaSerializer | Persona | — |
| PersonaEpSerializer | PersonaEp | — |
| PersonaPSerializer | PersonaEp | idpersona → PersonaSerializer |
| DireccionSerializer | Direccion | — |
| LocalidadSerializer | Localidad | — |
| MunicipioSerializer | Municipio | — |
| TipoparentescoSerializer | Tipoparentesco | — |

### 5.2. Módulo salud (7 serializadores)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| EvolucionSerializer | Evolucion | — |
| EnfermedadSerializer | Enfermedad | — |
| DiagnosticoSerializer | Diagnostico | — |
| DiagnosticoEpSerializer | Diagnostico | idenfermedad → EnfermedadSerializer |
| MedicamentoSerializer | Medicamento | — |
| IndicacionSerializer | Indicacionmedicamento | — |
| IndicacionEpSerializer | Indicacionmedicamento | idmedicamento → MedicamentoSerializer |

### 5.3. Módulo eventos (2 serializadores)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| TipoEventoSerializer | Tipoevento | — |
| EventoSerializer | Evento | 	ipoEvento → TipoEventoSerializer |

### 5.4. Módulo obra_social (3 serializadores)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| ObraSocialSerializer | Obrasocial | — |
| OSSerializer | Os | — |
| OSEpSerializer | Os | idobrasocial → ObraSocialSerializer |

### 5.5. Módulo talleres (11 serializadores)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| TallerSerializer | Taller | — |
| ClaseTallerSerializer | Clasetaller | — |
| ActividadSerializer | Actividad | — |
| ActividadRealizadaSerializer | Actividadrealizada | — |
| ComportamientoSerializer | Comportamiento | — |
| AsistenciaTallerSerializer | Asistenciataller | — |
| FactorClaseSerializer | Factorclase | — |
| FactorGlobalSerializer | Factorglobal | — |
| UnidadObservacionSerializer | Unidadobservacion | — |
| VariableUOSerializer | Variableuo | — |
| ValorVariableUOSerializer | Valorvariableuo | — |

## 6. Autenticación y Seguridad (core/authentication.py — 104 líneas)

- uth_view: POST /api/login — login con JWT (simplejwt)
- create_user: POST /api/create_user — solo superuser
- get_users: GET /api/users — listar usuarios (solo superuser)
- update_user: PUT /api/update_user — actualizar usuarios (solo superuser)
- efresh_token: POST /api/refresh_token — refresh JWT (TokenRefreshView de simplejwt)

> **Nota:** Todo movido de 	elepakApi/authentication.py → core/authentication.py.

## 7. Router Central (core/urls.py — 21 líneas)

`
core/urls.py
├── api/login                      → core.authentication.auth_view
├── api/create_user                → core.authentication.create_user
├── api/refresh_token              → TokenRefreshView (simplejwt)
├── api/users                      → core.authentication.get_users
├── api/update_user                → core.authentication.update_user
├── api/health                     → core.views.health_check
├── include('personas.urls')       → 7 endpoints
├── include('salud.urls')          → 5 endpoints
├── include('eventos.urls')        → 2 endpoints
├── include('obra_social.urls')    → 2 endpoints
└── include('talleres.urls')       → 11 endpoints
`

**Total endpoints expuestos:** 6 funcionales + 27 CRUD = 33 rutas (sin contar @action)

## 8. Configuración Django (telepark/settings.py — 190 líneas)

- **Apps instaladas:** django.contrib.[admin, auth, contenttypes, sessions, messages, staticfiles] + corsheaders + rest_framework + **core, personas, salud, eventos, obra_social, talleres**
- **Middleware:** CORS, Security, Session, Common, CSRF, Auth, Message, XFrame + **core.middleware.ExceptionMiddleware**
- **Auth:** JWTAuthentication (simplejwt), acceso 60min / refresh 1 día
- **BD:** MySQL (variables de entorno)
- **CORS:** CORS_ALLOWED_ORIGINS con SITE_URL desde variable de entorno

## 9. Hallazgos y Deuda Técnica Persistente

| ID | Hallazgo | Severidad | Archivo | Estado |
|----|----------|-----------|---------|--------|
| A003 | Lógica de negocio directa en authentication.py (validación inline en auth_view, create_user, update_user) | 🔴 Crítico | core/authentication.py | PERSISTE |
| B004 | Doble verificación de permisos: decorador @permission_classes([IsSuperuser]) + manual if not request.user.is_superuser en create_user, update_user, get_users | 🟡 Medio | core/authentication.py | PERSISTE |
| S004 | CSRF_TRUSTED_ORIGINS sin fallback — puede producir [None] si la variable no está definida | 🟡 Medio | telepark/settings.py | PERSISTE |
| M003 | Serializadores con anidación entre entidades del mismo módulo (ej: EventoSerializer anida TipoEventoSerializer). Ya no es acoplamiento cruzado entre dominios, pero persiste el patrón. | 🟢 Baja | varios serializers.py | PERSISTE PARCIALMENTE |
| DRY001 | BaseService, ServiceException y NotFoundException duplicados en 5 módulos de dominio. Deberían centralizarse en core/. | 🟡 Medio | personas, salud, eventos, obra_social, talleres/services.py | NUEVO |
| T001 | package-lock.json residual en la raíz del proyecto Django (sin package.json que lo justifique) | 🟢 Baja | package-lock.json | NUEVO |

### Hallazgos Resueltos desde 4991a18

| ID | Hallazgo | Resolución |
|----|----------|------------|
| M001 | Monolito: 26 modelos + 16 ViewSets + 15 servicios en un solo modulo | ✅ **RESUELTO** — Dividido en 6 módulos (core + 5 dominio) |
| M002 | Sin servicios para Talleres (11 modelos sin capa de negocio) | ✅ **RESUELTO** — 11 servicios creados en talleres/services.py |
| M004 | Todo el código de un dominio en archivos planos únicos | ✅ **RESUELTO** — Código distribuido en 6 módulos con estructura 3-layer |

## 10. Stack Tecnológico Confirmado

| Componente | Versión |
|-----------|---------|
| Python | 3.14.2 |
| Django | 6.0.6 |
| djangorestframework | 3.17.1 |
| djangorestframework-simplejwt | 5.4.0 |
| mysqlclient | 2.2.7 |
| django-cors-headers | 4.6.0 |
| python-dotenv | 1.0.1 |
| PyJWT | 2.10.1 |
| sqlparse | 0.5.3 |
| asgiref | 3.9.1 |
| cryptography | 44.0.0 |
| MySQL Server | 8.0.x (Docker) |
| Docker | ≥ 24.0 |
| Docker Compose | ≥ 2.20 |
