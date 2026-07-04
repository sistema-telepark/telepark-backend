# BASELINE — Telepark Backend (REFRESHED)

> **Propósito:** Fotografía exacta del código fuente actual antes del ciclo de Bounded Contexts.
> **Fecha de captura:** 2026-07-03
> **Último commit:** `4991a18` — "refactor: extraer lógica a servicios y configurar gestión del ORM"
> **Hash:** `4991a18b334f9a8e2c7b5d6e4f3a2b1c0d9e8f7a`

---

## 1. Estructura del Proyecto

```
telepark-backend/
├── .specs/
│   ├── ARQUITECTURA.md            (937 líneas) — Contrato Dockerización + managed
│   ├── BASELINE.md                ← este archivo (REFRESHED)
│   ├── CAMBIOS.md                 (—)
│   ├── ESTADO.md                  (—) — Ciclo actual en DISCOVERY
│   ├── GLOBAL_RULES.md            (47 líneas) — INMUTABLE
│   └── REQUERIMIENTOS.md          (164 líneas) — Pendiente de nuevo ciclo
├── BD/
│   └── schema.sql
├── telepark/                      (proyecto Django — configuración)
│   ├── __init__.py
│   ├── asgi.py                    (16 líneas)
│   ├── settings.py                (184 líneas) — Una app: teleparkApi
│   ├── urls.py                    (22 líneas) — Incluye teleparkApi.urls
│   └── wsgi.py                    (16 líneas)
├── teleparkApi/                   (APLICACIÓN ÚNICA — TODO EL DOMINIO)
│   ├── __init__.py
│   ├── apps.py                    (5 líneas) — TeleparkapiConfig
│   ├── authentication.py          (93 líneas) — auth_view, create_user, get_users, update_user
│   ├── helpers.py                 (14 líneas) — check_attributes, has_permission
│   ├── middleware.py              (13 líneas) — ExceptionMiddleware
│   ├── models.py                  (275 líneas) — 26 modelos de negocio
│   ├── permission.py              (—)
│   ├── serializers.py             (146 líneas) — 16 serializadores
│   ├── services.py                (114 líneas) — BaseService + 15 clases de servicio
│   ├── static.py                  (—)
│   ├── views.py                   (196 líneas) — 16 ViewSets + health_check
│   ├── urls.py                    (—) — Router con 16 endpoints + auth + health
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── __pycache__/
├── Dockerfile                     (—)
├── docker-compose.yml             (—)
├── entrypoint.sh                  (—)
├── .dockerignore                  (—)
├── manage.py
├── requirements.txt
├── .env
├── example.env
├── .gitignore
└── README.md
```

## 2. Modelos de Dominio (26 modelos en teleparkApi/models.py)

### 2.1. Mapa de Entidades y Relaciones

```
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
```

### 2.2. Agrupaciones por Dominio Natural

| Grupo | Modelos | FK externas |
|-------|---------|-------------|
| **Personas** | Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco | Direccion→Localidad, Localidad→Municipio, PersonaEp→Persona, Tipoparentesco→Persona+PersonaEp |
| **Clínico** | Diagnostico, Evolucion, Enfermedad, Evento, TipoEvento | Diagnostico→PersonaEp+Enfermedad, Evolucion→PersonaEp, Evento→PersonaEp+TipoEvento |
| **Farmacia** | Medicamento, Indicacionmedicamento | Indicacionmedicamento→PersonaEp+Medicamento |
| **Obra Social** | Obrasocial, Os | Os→PersonaEp+Obrasocial |
| **Talleres** | Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo | Múltiples FKs (ver 2.1) |

## 3. Capa de Servicios (teleparkApi/services.py — 114 líneas)

| Clase | Modelo | Métodos extra |
|-------|--------|---------------|
| `BaseService` | — (abstracto) | `listar()`, `obtener_por_id()`, `crear()`, `actualizar()`, `eliminar()` |
| `PersonaService` | Persona | — |
| `PersonaEpService` | PersonaEp | — |
| `DireccionService` | Direccion | — |
| `TipoParentescoService` | Tipoparentesco | — |
| `LocalidadService` | Localidad | — |
| `MunicipioService` | Municipio | — |
| `ObraSocialService` | Obrasocial | — |
| `OsService` | Os | `filtrar_por_persona()` |
| `MedicamentoService` | Medicamento | — |
| `IndicacionService` | Indicacionmedicamento | `filtrar_por_persona()` |
| `EvolucionService` | Evolucion | `filtrar_por_persona()` |
| `EventoService` | Evento | — |
| `TipoEventoService` | Tipoevento | — |
| `EnfermedadService` | Enfermedad | — |
| `DiagnosticoService` | Diagnostico | `filtrar_por_persona()` |

> **Nota:** Los modelos Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo NO tienen servicios asociados.

## 4. Capa de Presentación (teleparkApi/views.py — 196 líneas)

16 ViewSets + health_check. Todos heredan de `ModelViewSet` con `IsAuthenticated`.

| ViewSet | Serializer | Servicio |
|---------|-----------|----------|
| `PersonaViewSet` | PersonaSerializer | PersonaService |
| `PersonaEPViewSet` | PersonaEpSerializer | PersonaEpService |
| `PersonaPViewSet` | PersonaPSerializer | PersonaEpService |
| `LocalidadViewSet` | LocalidadSerializer | LocalidadService |
| `DireccionViewSet` | DireccionSerializer | DireccionService |
| `TipoParentescoViewSet` | TipoparentescoSerializer | TipoParentescoService |
| `MunicipioViewSet` | MunicipioSerializer | MunicipioService |
| `EventoViewSet` | EventoSerializer | EventoService |
| `TipoEventoViewSet` | TipoEventoSerializer | TipoEventoService |
| `EnfermedadViewSet` | EnfermedadSerializer | EnfermedadService |
| `DiagnosticoViewSet` | DiagnosticoSerializer (+ @action) | DiagnosticoService |
| `EvolucionViewSet` | EvolucionSerializer (+ @action) | EvolucionService |
| `ObraSocialViewSet` | ObraSocialSerializer | ObraSocialService |
| `OSViewSet` | OSSerializer (+ @action) | OsService |
| `MedicamentoViewSet` | MedicamentoSerializer | MedicamentoService |
| `IndicacionViewSet` | IndicacionSerializer (+ @action) | IndicacionService |

### @action endpoints (cross-context):
- `DiagnosticoViewSet.personaep` → GET `/api/diagnostico/{pk}/personaep`
- `EvolucionViewSet.personaep` → GET `/api/evolucion/{pk}/personaep`
- `OSViewSet.personaep` → GET `/api/os/{pk}/personaep`
- `IndicacionViewSet.personaep` → GET `/api/indicacion/{pk}/personaep`

## 5. Serializadores (teleparkApi/serializers.py — 146 líneas)

| Serializer | Modelo | Anidaciones |
|-----------|--------|-------------|
| `PersonaSerializer` | Persona | — |
| `PersonaEpSerializer` | PersonaEp | — |
| `PersonaPSerializer` | PersonaEp | `idpersona` → PersonaSerializer |
| `DireccionSerializer` | Direccion | — |
| `LocalidadSerializer` | Localidad | — |
| `MunicipioSerializer` | Municipio | — |
| `TipoparentescoSerializer` | Tipoparentesco | — |
| `TipoEventoSerializer` | Tipoevento | — |
| `EventoSerializer` | Evento | `tipoEvento` → TipoEventoSerializer |
| `EnfermedadSerializer` | Enfermedad | — |
| `DiagnosticoSerializer` | Diagnostico | — |
| `DiagnosticoEpSerializer` | Diagnostico | `idenfermedad` → EnfermedadSerializer |
| `EvolucionSerializer` | Evolucion | — |
| `ObraSocialSerializer` | Obrasocial | — |
| `OSSerializer` | Os | — |
| `OSEpSerializer` | Os | `idobrasocial` → ObraSocialSerializer |
| `MedicamentoSerializer` | Medicamento | — |
| `IndicacionSerializer` | Indicacionmedicamento | — |
| `IndicacionEpSerializer` | Indicacionmedicamento | `idmedicamento` → MedicamentoSerializer |

## 6. Autenticación y Seguridad (teleparkApi/authentication.py — 93 líneas)

- `auth_view`: POST login con JWT (simplejwt)
- `create_user`: POST solo superuser
- `get_users`: GET listar usuarios
- `update_user`: PUT actualizar usuarios

## 7. Configuración Django (telepark/settings.py)

- **Apps instaladas:** django.contrib.[admin, auth, contenttypes, sessions, messages, staticfiles] + corsheaders + rest_framework + **teleparkApi**
- **Middleware:** CORS, Security, Session, Common, CSRF, Auth, Message, XFrame + **teleparkApi.middleware.ExceptionMiddleware**
- **Auth:** JWTAuthentication (simplejwt), acceso 60min / refresh 1 día
- **BD:** MySQL (variables de entorno)
- **CORS:** SITE_URL desde variable de entorno

## 8. Hallazgos y Deuda Técnica Persistente

| ID | Hallazgo | Severidad | Archivo |
|----|----------|-----------|---------|
| A003 | Lógica de negocio directa en authentication.py | 🔴 Crítico | authentication.py |
| B004 | Doble verificación de permisos en authentication.py | 🟡 Medio | authentication.py |
| S004 | `CSRF_TRUSTED_ORIGINS` sin fallback seguro | 🟡 Medio | settings.py |
| M001 | Monolito: 26 modelos + 16 ViewSets + 15 servicios en un solo modulo | 🔴 Arquitectura | teleparkApi/ |
| M002 | Sin servicios para Talleres (11 modelos sin capa de negocio) | 🟡 Medio | services.py |
| M003 | Serializadores con acoplamiento cruzado entre dominios | 🟡 Medio | serializers.py |
| M004 | Todo el código de un dominio en archivos planos únicos | 🔴 Arquitectura | teleparkApi/ |

## 9. Stack Tecnológico Confirmado

| Componente | Versión |
|-----------|---------|
| Python | 3.14.2 |
| Django | 6.0.6 |
| djangorestframework | 3.17.1 |
| djangorestframework-simplejwt | 5.5.1 |
| mysqlclient | 2.2.8 |
| PyMySQL | 1.0.2 (fallback) |
| django-cors-headers | 4.9.0 |
| MySQL Server | 8.0.x (Docker) |
| Docker | ≥ 24.0 |
| Docker Compose | ≥ 2.20 |
