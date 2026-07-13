# MEMORIA DE BASELINE DE PROYECTO

> **Metadatos de Control de Vigencia**
> - **Fecha de Analisis:** 2026-07-13
> - **Origen del Escaneo:** `16e9215222680d07ab3b520c5c20c3eedd5a47a6` (HEAD)
> - **Verificacion:** `git rev-parse HEAD` -> `16e9215222680d07ab3b520c5c20c3eedd5a47a6`

---

## 1. Resumen Ejecutivo

Telepark Backend es un sistema **Django 6.0.6 / DRF 3.17.1 / MySQL 8.4** compuesto por **7 apps Django** (autenticacion, core, personas, salud, eventos, obra_social, talleres) que implementan un backend REST para gestion de personas, salud, eventos, obras sociales y talleres terapeuticos. El proyecto se ejecuta en Docker con auto-generacion de migraciones en entrypoint.

**Cambios post-cc251eb (2 commits):**

- **Commit `61f41c5`** — Refactor de endpoints `personaEp`: los 4 endpoints `@action` en salud y obra_social (rutas semanticamente incorrectas `/api/{recurso}/{pk}/personaep`) fueron reemplazados por **4 APIViews** con rutas correctas bajo `/api/personaEp/{personaep_pk}/`. Se actualizo `auto_tag_schema_view` en `core/mixins.py` para etiquetar tambien `@action` residuales. El `docker-compose.yml` fue actualizado de MySQL 8.0 a 8.4 en este commit.

- **Commit `16e9215`** — Upgrade MySQL 8.0 -> 8.4 en `Dockerfile` y `README.md`. Sequito de seguridad en `bootstrap_admin.py`: la contrasena de admin ya no se imprime en stdout.

**Estado actual:** 27 ViewSets (14 con paginacion global, 13 con opt-out por ser catalogos), 6 function views (5 auth + 1 health), 0 endpoints `@action`, 4 APIViews (GenericAPIView) para sub-recursos de PersonaEp. Migraciones auto-generadas en entrypoint.sh.

**Deuda tecnica remanente:** (1) ausencia total de tests, (2) `SECRET_KEY` con fallback hardcodeado en docker-compose, (3) `BaseService.actualizar()` sin `update_fields`, (4) `EvolucionService.filtrar_por_persona()` sin `select_related`, (5) paginacion manual en `get_users` de autenticacion (inconsistencia con patron global), (6) 4 APIViews de sub-recursos sin paginacion, (7) `CORS_ALLOWED_ORIGINS` vulnerable a `[None]` si falta env var.

---

## 2. Stack Tecnologico

| Componente | Version | Detalle |
|---|---|---|
| Python | 3.14.2 | `python:3.14-slim` (Docker) |
| Django | 6.0.6 | `Django==6.0.6` |
| djangorestframework | 3.17.1 | `djangorestframework==3.17.1` |
| djangorestframework-simplejwt | 5.4.0 | JWT auth (access 60m, refresh 1d, `USER_ID_FIELD='username'`) |
| drf-spectacular | 0.29.0 | OpenAPI 3.0 schema en `/api/schema/swagger-ui/` |
| mysqlclient | 2.2.7 | Driver MySQL |
| django-cors-headers | 4.6.0 | CORS middleware |
| python-dotenv | 1.0.1 | Env vars |
| PyJWT | 2.10.1 | Token JWT |
| cryptography | 44.0.0 | Crypto subyacente |
| MySQL Server | 8.4.x | Docker, puerto host `3307` (upgraded from 8.0 en 61f41c5/16e9215) |
| Docker | -- | Dockerfile + docker-compose.yml (puerto host `8081`) |
| Build | pip | `requirements.txt` con versiones fijas |

**Nota:** El proyecto fue scaffold originalmente con `django-admin startproject` en Django 3.2 y posteriormente actualizado a 6.0.6.

---

## 3. Topologia de Modulos

### Patron: Monolito Modular con Capa de Servicios

```
+------------------------------------------------------------------+
|  URLs (urls.py c/app) -- DefaultRouter, rutas /api/*              |
|  core/urls.py -- router central que agrega todos los             |
|                  modulos + auth + docs + health +                 |
|                  rutas /api/personaEp/{pk}/* (APIViews)           |
+------------------------------------------------------------------+
|  Views (views.py) -- 27 ModelViewSet                             |
|                       + 6 function views + 1 TokenRefreshView     |
|                       + 4 APIViews (GenericAPIView)               |
|      -> todos heredan de ModelPKMixin                             |
|      -> service = _xxx_service para introspeccion                 |
+------------------------------------------------------------------+
|  Serializers (serializers.py) -- ModelSerializer                  |
|                      + Serializer planos (auth)                   |
+------------------------------------------------------------------+
|  Services (services.py) -- Logica de negocio                     |
|  core/services.py     -- BaseService generico CRUD               |
|  core/exceptions.py   -- ServiceException base                   |
|                      + 5 excepciones de dominio                  |
|  core/mixins.py       -- ModelPKMixin, NoPaginationMixin,        |
|                          auto_tag_schema_view                    |
+------------------------------------------------------------------+
|  Models (models.py) -- 26 modelos, MySQL legacy                  |
+------------------------------------------------------------------+
```

### DAG de Dependencias (Aciclico)

```
autenticacion/     (auth wrapper, sin models propios) -> django.contrib.auth.User
core/              (infra: middleware, permissions, router, health, BaseService, exceptions, mixins)
personas/          (6 modelos) <- raiz de dominio, sin dependencias externas
salud/             (5 modelos) -> personas (FK a PersonaEp)
eventos/           (2 modelos) -> personas (FK a PersonaEp)
obra_social/       (2 modelos) -> personas (FK a PersonaEp)
talleres/          (11 modelos) -> personas (FK a PersonaEp)
```

### Capas por Modulo

| Modulo | Services | Views | Serializers | Models | Mixins |
|---|---|---|---|---|---|
| autenticacion | `UsuarioService` (5 metodos static) | 5 @api_view + 1 TokenRefreshView | 5 serializers | -- (usa `django.contrib.auth.User`) | -- |
| core | `BaseService` (6 metodos CRUD) + 5 excepciones | 1 function view (`health_check`) | -- | -- | `ModelPKMixin`, `NoPaginationMixin`, `auto_tag_schema_view` |
| personas | 6 services (herencia `core.BaseService`) | 7 ModelViewSet | 7 serializers | 6 modelos | -- |
| salud | 5 services (herencia `core.BaseService`) | 5 ModelViewSet + 3 APIViews | 7 serializers | 5 modelos | -- |
| eventos | 2 services (herencia `core.BaseService`) | 2 ModelViewSet | 2 serializers | 2 modelos | -- |
| obra_social | 2 services (herencia `core.BaseService`) | 2 ModelViewSet + 1 APIView | 3 serializers | 2 modelos | -- |
| talleres | 11 services (herencia `core.BaseService`) | 11 ModelViewSet | 11 serializers | 11 modelos | -- |

---

## 4. Modelos por App

### 4.1. personas -- 6 modelos

| Modelo | Campos clave |
|---|---|
| `Persona` | `idpersona` (PK), `nombre`, `apellido`, `telefono`, `iddireccion` (FK->Direccion), `borrado`, `espaciente` |
| `PersonaEp` | `idpersona` (PK, FK->Persona, OneToOne), `idreferente` (FK->Persona), `fechainicio`, `fechanacimiento`, `sexo`, `activataller`, `escolaridadcompleta`, `maximaescolaridadalcanzada`, `tieneacompanante`, `tienecuidador`, `vivesolo`, `ocupacionprevia`, `ocupacionactual` |
| `Direccion` | `iddireccion` (PK), `calle`, `departamento`, `numero`, `piso`, `idlocalidad` (FK->Localidad) |
| `Localidad` | `idlocalidad` (PK), `nombre`, `codigopostal`, `idmunicipio` (FK->Municipio) |
| `Municipio` | `idmunicipio` (PK), `nombre`, `provincia` |
| `Tipoparentesco` | `idtipoparentesco` (PK, AutoField), `idpersona` (FK->Persona), `idpersonaep` (FK->PersonaEp), `nombre` |

### 4.2. salud -- 5 modelos

| Modelo | Campos clave |
|---|---|
| `Diagnostico` | `iddiagnostico` (PK), `fecha`, `idpersonaep` (FK->PersonaEp), `idenfermedad` (FK->Enfermedad), `borrado` |
| `Evolucion` | `idevolucion` (PK), `escalaevolucion`, `fecha`, `idpersonaep` (FK->PersonaEp), `borrado` |
| `Enfermedad` | `idenfermedad` (PK), `nombre` |
| `Medicamento` | `idmedicamento` (PK), `nombre`, `esantiparkinsoniano`, `eslevodopa` |
| `Indicacionmedicamento` | `idindicacion` (PK), `cantidadmiligramos`, `estavigente`, `fechaprescripcion`, `horadetoma`, `idpersonaep` (FK->PersonaEp), `idmedicamento` (FK->Medicamento), `borrado` |

### 4.3. eventos -- 2 modelos

| Modelo | Campos clave |
|---|---|
| `Tipoevento` | `idtipoevento` (PK), `nombre`, `desactivataller`, `borrado` |
| `Evento` | `idevento` (PK), `fechadesde`, `fechahasta`, `motivo`, `idpersonaep` (FK->PersonaEp), `idtipoevento` (FK->Tipoevento), `borrado` |

### 4.4. obra_social -- 2 modelos

| Modelo | Campos clave |
|---|---|
| `Obrasocial` | `idobrasocial` (PK), `nombre`, `esestatal` |
| `Os` | `idos` (PK), `idpersonaep` (FK->PersonaEp), `idobrasocial` (FK->Obrasocial), `borrado` |

### 4.5. talleres -- 11 modelos

| Modelo | Campos clave |
|---|---|
| `Taller` | `idtaller` (PK), `tipotaller` |
| `Clasetaller` | `idclasetaller` (PK), `fecha`, `virtual`, `idtaller` (FK->Taller) |
| `Actividad` | `idactividad` (PK), `nombre`, `idtaller` (FK->Taller) |
| `Actividadrealizada` | `idactividad` (PK, FK->Actividad, OneToOne), `idclasetaller` (FK->Clasetaller) |
| `Comportamiento` | `idcomportamiento` (PK), `comentario` |
| `Asistenciataller` | `idasistenciataller` (PK), `estado`, `idpersonaep` (FK->PersonaEp), `idclasetaller` (FK->Clasetaller), `idcomportamiento` (FK->Comportamiento) |
| `Factorclase` | `idclasetaller` (PK, FK->Clasetaller, OneToOne), `idfactorglobal` (FK->Factorglobal) |
| `Factorglobal` | `idfactorglobal` (PK), `nombre` |
| `Unidadobservacion` | `idunidadobservacion` (PK), `nombre` |
| `Variableuo` | `idvariableuo` (PK), `nombre`, `idcomportamiento` (FK->Comportamiento), `idunidadobservacion` (FK->Unidadobservacion) |
| `Valorvariableuo` | `idvalorvariableuo` (PK), `valor`, `idvariableuo` (FK->Variableuo) |

---

## 5. Catalogo de ViewSets y Configuracion de Paginacion

### 5.1. Vista General

| Tipo | Cantidad | Mecanismo de Paginacion |
|---|---|---|
| ViewSets con paginacion global (DRF default, PageNumberPagination, page_size=50) | 14 | `DEFAULT_PAGINATION_CLASS` -- todos con orden deterministico |
| ViewSets con opt-out (catalogos) | 13 | `NoPaginationMixin` (`pagination_class = None`) |
| Function views manuales | 1 | `PageNumberPagination` explicito (page_size=50) en `get_users` |
| APIView endpoints (sub-recursos PersonaEp) | 4 | Sin paginacion explicita |

### 5.2. Personas -- 7 ViewSets

| ViewSet | Paginacion | Motivo |
|---|---|---|
| `PersonaViewSet` | Global (page_size=50) | Datos transaccionales |
| `PersonaEPViewSet` | Global (page_size=50) | Datos transaccionales |
| `PersonaPViewSet` | Global (page_size=50) | Datos transaccionales |
| `DireccionViewSet` | Global (page_size=50) | Datos transaccionales |
| `TipoParentescoViewSet` | **Opt-out** (None) | Catalogo pequeno |
| `LocalidadViewSet` | **Opt-out** (None) | Catalogo |
| `MunicipioViewSet` | **Opt-out** (None) | Catalogo |

### 5.3. Salud -- 5 ViewSets + 3 APIViews

| ViewSet | Paginacion |
|---|---|
| `DiagnosticoViewSet` | Global (page_size=50) |
| `EvolucionViewSet` | Global (page_size=50) |
| `IndicacionViewSet` | Global (page_size=50) |
| `EnfermedadViewSet` | **Opt-out** (None) |
| `MedicamentoViewSet` | **Opt-out** (None) |

Endpoints APIView (sub-recursos PersonaEp):
- `DiagnosticoPorPersonaEpView` (GET /api/personaEp/{personaep_pk}/diagnostico) -- Sin paginacion
- `EvolucionPorPersonaEpView` (GET /api/personaEp/{personaep_pk}/evolucion) -- Sin paginacion
- `IndicacionPorPersonaEpView` (GET /api/personaEp/{personaep_pk}/indicacion) -- Sin paginacion

### 5.4. Eventos -- 2 ViewSets

| ViewSet | Paginacion |
|---|---|
| `EventoViewSet` | Global (page_size=50) |
| `TipoEventoViewSet` | **Opt-out** (None) |

### 5.5. Obra Social -- 2 ViewSets + 1 APIView

| ViewSet | Paginacion |
|---|---|
| `ObraSocialViewSet` | **Opt-out** (None) |
| `OSViewSet` | **Opt-out** (None) |

Endpoint APIView (sub-recurso PersonaEp):
- `OsPorPersonaEpView` (GET /api/personaEp/{personaep_pk}/os) -- Sin paginacion

### 5.6. Talleres -- 11 ViewSets

| ViewSet | Paginacion | Motivo |
|---|---|---|
| `TallerViewSet` | Global (page_size=50) | Datos transaccionales |
| `ClaseTallerViewSet` | Global (page_size=50) | Datos transaccionales |
| `ActividadViewSet` | Global (page_size=50) | Datos transaccionales |
| `ActividadRealizadaViewSet` | Global (page_size=50) | Datos transaccionales |
| `AsistenciaTallerViewSet` | Global (page_size=50) | Datos transaccionales |
| `ValorVariableUOViewSet` | Global (page_size=50) | Datos transaccionales |
| `ComportamientoViewSet` | **Opt-out** (None) | Catalogo |
| `FactorClaseViewSet` | **Opt-out** (None) | Catalogo |
| `FactorGlobalViewSet` | **Opt-out** (None) | Catalogo |
| `UnidadObservacionViewSet` | **Opt-out** (None) | Catalogo |
| `VariableUOViewSet` | **Opt-out** (None) | Catalogo |

### 5.7. Autenticacion -- Endpoints No-ViewSet

| Endpoint | Tipo | Paginacion |
|---|---|---|
| `auth_view` | @api_view POST | N/A (login) |
| `create_user` | @api_view POST | N/A |
| `update_user` | @api_view PUT | N/A |
| `get_users` | @api_view GET | Manual: `PageNumberPagination()`, page_size=50 |
| `change_user_role` | @api_view PUT | N/A |
| `TokenRefreshView` | TokenRefreshView POST | N/A |

---

## 6. Mapa de Endpoints

### 6.1. Sistema

| Metodo | Ruta | Vista | Permiso | Paginacion |
|---|---|---|---|---|
| GET | `/api/health` | `health_check` | AllowAny | N/A |

### 6.2. Autenticacion

| Metodo | Ruta | Vista | Permiso | Paginacion |
|---|---|---|---|---|
| POST | `/api/login` | `auth_view` | AllowAny | N/A |
| POST | `/api/create_user` | `create_user` | IsSuperuser | N/A |
| PUT | `/api/update_user` | `update_user` | IsSuperuser | N/A |
| GET | `/api/users` | `get_users` | IsSuperuser | Manual PageNumberPagination (50) |
| PUT | `/api/users/<str:username>/role` | `change_user_role` | IsSuperuser | N/A |
| POST | `/api/refresh_token` | `TokenRefreshView` | AllowAny | N/A |

### 6.3. Personas

| Metodo | Ruta | ViewSet | Paginacion |
|---|---|---|---|
| CRUD | `/api/persona` | PersonaViewSet | Global (50) |
| CRUD | `/api/personaEp` | PersonaEPViewSet | Global (50) |
| CRUD | `/api/personaP` | PersonaPViewSet | Global (50) |
| CRUD | `/api/direccion` | DireccionViewSet | Global (50) |
| CRUD | `/api/tipoparentesco` | TipoParentescoViewSet | **Opt-out** |
| CRUD | `/api/localidad` | LocalidadViewSet | **Opt-out** |
| CRUD | `/api/municipio` | MunicipioViewSet | **Opt-out** |

### 6.4. Salud

| Metodo | Ruta | ViewSet/View | Paginacion |
|---|---|---|---|
| CRUD | `/api/diagnostico` | DiagnosticoViewSet | Global (50) |
| CRUD | `/api/evolucion` | EvolucionViewSet | Global (50) |
| CRUD | `/api/indicacion` | IndicacionViewSet | Global (50) |
| CRUD | `/api/enfermedad` | EnfermedadViewSet | **Opt-out** |
| CRUD | `/api/medicamento` | MedicamentoViewSet | **Opt-out** |
| GET | `/api/personaEp/{personaep_pk}/diagnostico` | DiagnosticoPorPersonaEpView | Sin paginacion |
| GET | `/api/personaEp/{personaep_pk}/evolucion` | EvolucionPorPersonaEpView | Sin paginacion |
| GET | `/api/personaEp/{personaep_pk}/indicacion` | IndicacionPorPersonaEpView | Sin paginacion |

### 6.5. Eventos

| Metodo | Ruta | ViewSet | Paginacion |
|---|---|---|---|
| CRUD | `/api/evento` | EventoViewSet | Global (50) |
| CRUD | `/api/tipoevento` | TipoEventoViewSet | **Opt-out** |

### 6.6. Obra Social

| Metodo | Ruta | ViewSet/View | Paginacion |
|---|---|---|---|
| CRUD | `/api/obrasocial` | ObraSocialViewSet | **Opt-out** |
| CRUD | `/api/os` | OSViewSet | **Opt-out** |
| GET | `/api/personaEp/{personaep_pk}/os` | OsPorPersonaEpView | Sin paginacion |

### 6.7. Talleres

| Metodo | Ruta | ViewSet | Paginacion |
|---|---|---|---|
| CRUD | `/api/taller` | TallerViewSet | Global (50) |
| CRUD | `/api/clasetaller` | ClaseTallerViewSet | Global (50) |
| CRUD | `/api/actividad` | ActividadViewSet | Global (50) |
| CRUD | `/api/actividadrealizada` | ActividadRealizadaViewSet | Global (50) |
| CRUD | `/api/asistenciataller` | AsistenciaTallerViewSet | Global (50) |
| CRUD | `/api/valorvariableuo` | ValorVariableUOViewSet | Global (50) |
| CRUD | `/api/comportamiento` | ComportamientoViewSet | **Opt-out** |
| CRUD | `/api/factorclase` | FactorClaseViewSet | **Opt-out** |
| CRUD | `/api/factorglobal` | FactorGlobalViewSet | **Opt-out** |
| CRUD | `/api/unidadobservacion` | UnidadObservacionViewSet | **Opt-out** |
| CRUD | `/api/variableuo` | VariableUOViewSet | **Opt-out** |

### 6.8. Documentacion

| Metodo | Ruta | Vista | Permiso (dev) | Permiso (prod) |
|---|---|---|---|---|
| GET | `/api/schema/` | SpectacularAPIView | AllowAny | IsAdminUser |
| GET | `/api/schema/swagger-ui/` | SpectacularSwaggerView | AllowAny | IsAdminUser |
| GET | `/api/schema/redoc/` | SpectacularRedocView | AllowAny | IsAdminUser |

---

## 7. Configuracion de Django/DRF

### 7.1. REST_FRAMEWORK (settings.py:113-121)

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```

14 ViewSets de dominio transaccional heredan esta configuracion. 13 ViewSets de catalogo la deshabilitan via `NoPaginationMixin`.

### 7.2. JWT (settings.py:148-172)

- `ACCESS_TOKEN_LIFETIME`: 60 minutos
- `REFRESH_TOKEN_LIFETIME`: 1 dia
- `ROTATE_REFRESH_TOKENS`: False
- `USER_ID_FIELD`: `'username'`
- `AUTH_HEADER_TYPES`: `('Bearer',)`

### 7.3. SPECTACULAR_SETTINGS (settings.py:123-146)

- TAGS por modulo: sistema, autenticacion, personas, salud, eventos, obra_social, talleres
- `SCHEMA_PATH_PREFIX`: `r'/api/'`
- Security: `BearerAuth`
- En produccion: `SERVE_PERMISSIONS = [IsAdminUser]`

### 7.4. Base de Datos (settings.py:102-111)

- Motor: MySQL 8.4 (upgraded from 8.0 en commits 61f41c5/16e9215)
- Host/Port desde env vars (Docker: db:3306, Host: localhost:3307)

### 7.5. Middleware (settings.py:67-77)

- `corsheaders.middleware.CorsMiddleware` (primero)
- `core.middleware.ExceptionMiddleware` (ultimo) -- captura excepciones no manejadas -> JSON con codigo HTTP correcto

### 7.6. ExceptionMiddleware (core/middleware.py:16-43)

Mapeo de excepciones a codigos HTTP:

| Excepcion | HTTP Status |
|---|---|
| `NotFoundException` | 404 |
| `ValidationError` | 400 |
| `PermissionDeniedError` | 403 |
| `ConflictError` | 409 |
| `AuthenticationError` | 401 |
| Cualquier otra | 500 (con `repr(exception)` + logging) |

### 7.7. Entrypoint (entrypoint.sh)

- `python manage.py check --deploy` (validacion estricta, WARNINGS filtrados)
- `python manage.py makemigrations --noinput` (auto-genera migraciones)
- `python manage.py migrate` (aplica)
- `python manage.py bootstrap_admin` (crea superadmin inicial, sin exponer password en stdout)
- `python manage.py runserver 0.0.0.0:8080`

---

## 8. Inventario de Servicios

### 8.1. Core (`core/services.py` + `core/exceptions.py` + `core/mixins.py`)

**`core/exceptions.py`** -- Excepciones base de dominio:

| Clase | Padre | Proposito |
|---|---|---|
| `ServiceException` | `Exception` | Base para todas las excepciones de servicio |
| `NotFoundException` | `ServiceException` | Recurso no encontrado |
| `AuthenticationError` | `ServiceException` | Error de autenticacion |
| `ValidationError` | `ServiceException` | Error de validacion |
| `PermissionDeniedError` | `ServiceException` | Permiso denegado |
| `ConflictError` | `ServiceException` | Conflicto (ej. ultimo admin) |

**`core/services.py`** -- `BaseService` generico:

| Metodo | Comportamiento |
|---|---|
| `listar()` | `self.model.objects.all().order_by(self.model._meta.pk.name)` -- orden deterministico por PK |
| `obtener_por_id(pk)` | `self.model.objects.get(pk=pk)` -- lanza `NotFoundException` |
| `crear(**datos)` | `self.model.objects.create(**datos)` |
| `actualizar(pk, **datos)` | Obtiene por id, aplica `setattr` + `obj.save()` (sin `update_fields`) |
| `eliminar(pk)` | Obtiene por id, ejecuta `obj.delete()` |
| `filtrar_por_persona(personaep_pk, select_related_fields=None)` | Filtra por `idpersonaep`, con `select_related` opcional |

**`core/mixins.py`** -- Mixins de infraestructura:

| Clase | Atributos/Metodos clave |
|---|---|
| `ModelPKMixin` | `lookup_field = 'pk'`, `service = None`, `app_tag = None`; property `queryset` retorna `none()` para introspeccion; `get_queryset()` delega a `self.service.listar()` |
| `NoPaginationMixin` | `pagination_class = None` |
| `auto_tag_schema_view(cls)` | Decorador que aplica `@extend_schema_view` con tag basado en `cls.app_tag`. Ademas etiqueta metodos `@action` residuales (defensivo). |

### 8.2. Autenticacion (`autenticacion/services.py`)

Clase `UsuarioService` (todos los metodos static):

| Metodo | Query | Excepciones lanzadas |
|---|---|---|
| `autenticar(data)` | `User.objects.get(username=...)` | `AuthenticationError` |
| `crear(data)` | `User.objects.filter(...)`, `User.objects.create_user(...)` | `ValidationError` |
| `actualizar(data)` | `User.objects.get(username=...)`, `user.save()` | `ValidationError` |
| `listar(filters)` | `User.objects.all().order_by('id')` + filtros Q | -- |
| `cambiar_rol(actor, target, is_superuser)` | `User.objects.get(username=...)`, `User.objects.filter(...)` | `NotFoundException`, `PermissionDeniedError`, `ConflictError` |

### 8.3. Personas (`personas/services.py`)

Todos heredan de `core.BaseService`:

| Servicio | Modelo | Metodos override | `select_related` |
|---|---|---|---|
| `PersonaService` | `Persona` | -- | No |
| `PersonaEpService` | `PersonaEp` | `listar()` (order_by `idpersona`, hereda orden PK) | `select_related('idpersona')` |
| `DireccionService` | `Direccion` | -- | No |
| `TipoParentescoService` | `Tipoparentesco` | -- | No |
| `LocalidadService` | `Localidad` | -- | No |
| `MunicipioService` | `Municipio` | -- | No |

### 8.4. Salud (`salud/services.py`)

Todos heredan de `core.BaseService`:

| Servicio | Modelo | Metodos override | `select_related` |
|---|---|---|---|
| `DiagnosticoService` | `Diagnostico` | `listar()` (order_by `idpersonaep`, `iddiagnostico`) | En `filtrar_por_persona` via parametro desde view/APIView |
| `EvolucionService` | `Evolucion` | `listar()` (order_by `idpersonaep`, `idevolucion`) | No (llamada desde APIView sin `select_related_fields`) |
| `EnfermedadService` | `Enfermedad` | -- | No |
| `MedicamentoService` | `Medicamento` | -- | No |
| `IndicacionService` | `Indicacionmedicamento` | `listar()` (order_by `idpersonaep`, `idindicacion`) | En `filtrar_por_persona` via parametro desde view/APIView |

### 8.5. Eventos (`eventos/services.py`)

Todos heredan de `core.BaseService`:

| Servicio | Modelo | Metodos override | `select_related` |
|---|---|---|---|
| `EventoService` | `Evento` | `listar()` (order_by `idpersonaep`, `idevento`) | `select_related('idtipoevento')` |
| `TipoEventoService` | `Tipoevento` | -- | No |

### 8.6. Obra Social (`obra_social/services.py`)

Todos heredan de `core.BaseService`:

| Servicio | Modelo | Metodos override | `select_related` |
|---|---|---|---|
| `ObraSocialService` | `Obrasocial` | -- | No |
| `OsService` | `Os` | -- | `filtrar_por_persona` heredado de BaseService con `select_related_fields` desde APIView |

### 8.7. Talleres (`talleres/services.py`)

Todos heredan de `core.BaseService`:

| Servicio | Modelo | Metodos override | `select_related` |
|---|---|---|---|
| `TallerService` | `Taller` | -- | No |
| `ClaseTallerService` | `Clasetaller` | -- | No |
| `ActividadService` | `Actividad` | -- | No |
| `ActividadRealizadaService` | `Actividadrealizada` | -- | No |
| `AsistenciaTallerService` | `Asistenciataller` | `listar()` (order_by `idpersonaep`, `idasistenciataller`) | No |
| `ComportamientoService` | `Comportamiento` | -- | No |
| `FactorClaseService` | `Factorclase` | -- | No |
| `FactorGlobalService` | `Factorglobal` | -- | No |
| `UnidadObservacionService` | `Unidadobservacion` | -- | No |
| `VariableUOService` | `Variableuo` | -- | No |
| `ValorVariableUOService` | `Valorvariableuo` | -- | No |

---

## 9. Patrones y Convenciones Verificadas

- **3-layer:** Views/Serializers -> Services -> Models. Desacoplamiento de DRF de Services verificado.
- **Cross-module FKs** usan string refs: `models.ForeignKey('personas.PersonaEp', ...)`
- **Router centralizado:** `core/urls.py` agrega `DefaultRouter`s de cada app + auth + docs + rutas directas de APIViews
- **Trailing slashes deshabilitados:** `DefaultRouter(trailing_slash=False)` en cada modulo
- **Rutas bajo `/api/`**
- **Autenticacion:** SimpleJWT (JWTAuthentication global via `REST_FRAMEWORK`)
- **Autorizacion:** `IsAuthenticated` para ViewSets de dominio, `IsSuperuser` para endpoints de gestion de usuarios
- **Paginacion global:** `PageNumberPagination` (page_size=50) con opt-out via `NoPaginationMixin` en 13 catalogos
- **Orden deterministico:** `BaseService.listar()` inyecta `.order_by(PK)`; servicios con FK a PersonaEp usan orden compuesto `idpersonaep` + PK
- **Middleware de errores:** `core.middleware.ExceptionMiddleware` captura excepciones `ServiceException` -> JSON con codigo HTTP correcto (404, 400, 403, 409, 401); resto -> 500
- **Sin suite de tests, linter, formatter ni type checker configurados**
- **Migraciones auto-generadas** en entrypoint.sh (`makemigrations --noinput` + `migrate`)
- **drf-spectacular** configurado con tags por modulo, `BearerAuth`, `SCHEMA_PATH_PREFIX='/api/'`
- **ModelPKMixin** en todos los ViewSets de dominio + `auto_tag_schema_view` decorator para tags automaticos (tambien cubre @action residuales)
- **`.gitignore` excluye `*migrations/`** -- las migraciones no se commitean
- **Convencion de nombres:** modelos y campos en snake_case con `db_column` en camelCase para reflejar MySQL legacy. Todos los nombres de campo de API en snake_case (incluyendo `tipo_evento` corregido).
- **Endpoint de sub-recursos PersonaEp:** las rutas `/api/personaEp/{personaep_pk}/` reemplazaron los `@action` con path semantico incorrecto. Ahora `{personaep_pk}` es el PK real de PersonaEp.
- **bootstrap_admin:** la contrasena de admin ya no se imprime en stdout (seguridad). `ADMIN_BOOTSTRAP_PASSWORD` ignorada en prod (genera token aleatorio).

---

## 10. Deuda Tecnica Conocida

### 10.1. Estado Post-Refactor (acumulado desde cc251eb + correcciones 61f41c5 + 16e9215)

| Hallazgo | Commit | Estado Actual |
|---|---|---|
| BaseService duplicado en 5 modulos | `05ba063` | CORREGIDO |
| 27 ViewSets con `queryset` de clase | `aba8547` | CORREGIDO |
| `EventoSerializer.tipoEvento` sin `source` | `253057b` | CORREGIDO |
| 5 N+1 queries sin `select_related` | `253057b` | CORREGIDO (parcial -- ver D07) |
| `autenticacion/services.py` acoplado a DRF | `643545b` | CORREGIDO |
| `UnorderedObjectListWarning` en GET /api/users | `253057b` | CORREGIDO |
| 27 warnings W001 de drf-spectacular | `253057b` | CORREGIDO |
| Security.WXXX sin documentar | `253057b` | DOCUMENTADO |
| App `usuarios` nombrada inconsistentemente | `136b758` | CORREGIDO |
| Sin paginacion global en ViewSets | `82f8202` | CORREGIDO |
| `UnorderedObjectListWarning` en 14 ViewSets paginados | `e65fbcd` | CORREGIDO |
| TD-01: 27 copias de `@extend_schema_view` repetido | `cc251eb` | CORREGIDO (via `auto_tag_schema_view`) |
| TD-02: `Tipoparentesco` con OneToOneField como PK | `cc251eb` | CORREGIDO (AutoField + ForeignKey) |
| TD-03: 26 `get_queryset()` identicos | `cc251eb` | CORREGIDO (centralizado en ModelPKMixin) |
| TD-04: ExceptionMiddleware siempre devuelve 500 | `cc251eb` | CORREGIDO (mapeo a 404, 400, 403, 409, 401) |
| TD-05: CSRF_TRUSTED_ORIGINS con `[None]` potencial | `cc251eb` | CORREGIDO (default + split) |
| TD-06: `tipoEvento` camelCase | `cc251eb` | CORREGIDO (`tipo_evento`) |
| TD-07: Unused imports en core/views.py | `cc251eb` | CORREGIDO |
| TD-08: `ServiceException` importado sin uso en 6 archivos | `cc251eb` | CORREGIDO |
| TD-09: `TokenRefreshViewWrapper` innecesario | `cc251eb` | CORREGIDO (decorador directo en urls.py) |
| TD-10: 13 `pagination_class = None` repetidos | `cc251eb` | CORREGIDO (via `NoPaginationMixin`) |
| TD-11: Pares de serializers casi identicos | `cc251eb` | CORREGIDO (herencia existente ya implementada) |
| TD-12: 4 `filtrar_por_persona` con misma logica | `cc251eb` | CORREGIDO (centralizado en BaseService) |
| TD-13: `STATIC_URL` duplicado | `cc251eb` | CORREGIDO |
| TD-14: Directorio `static/` vacio | Persiste | No afecta funcionalidad |
| TD-15: Directorio `BD/` con artefactos | Persiste | No afecta funcionalidad |
| TD-16: `package-lock.json` huerfano | Persiste | No afecta funcionalidad |
| TD-17: `.pyc` huerfanos | Persiste | No afecta funcionalidad |
| TD-18: Email hardcodeado `admin@telepark.com` | `cc251eb` | CORREGIDO (via `ADMIN_EMAIL` env var) |
| TD-19: `mimetypes.add_type` innecesario | `cc251eb` | CORREGIDO |
| TD-20: Mezcla `os.path`/`pathlib.Path` | `cc251eb` | CORREGIDO (uso consistente de `BASE_DIR / ...`) |
| TD-21: Password de admin expuesta en stdout en bootstrap_admin | `16e9215` | CORREGIDO (removida la impresion) |
| D05: 4 @action con path semantico incorrecto | `61f41c5` | CORREGIDO (reemplazados por APIViews con ruta correcta) |

### 10.2. Deuda Tecnica Vigente (Post-HEAD)

| ID | Prioridad | Descripcion | Archivos |
|---|---|---|---|
| D01 | ALTA | Sin suite de tests en todo el proyecto | -- |
| D02 | ALTA | `SECRET_KEY` con fallback hardcodeado en docker-compose.yml (`django-insecure-dev-key-not-for-production`) | `docker-compose.yml:37` |
| D03 | MEDIA | `BaseService.actualizar()` sin `update_fields` -- UPDATE completo en cada save | `core/services.py:21-26` |
| D07 | MEDIA | `EvolucionService.filtrar_por_persona()` llamado sin `select_related_fields` desde `salud/views.py:90` (EvolucionPorPersonaEpView) -- N+1 potencial | `salud/views.py:90` |
| D09 | BAJA | `get_users` en autenticacion usa paginacion manual inconsistente con el patron global (`PageNumberPagination()` explicito en vez de heredar DRF default) | `autenticacion/views.py:181-185` |
| D10 | BAJA | 4 APIViews de sub-recursos PersonaEp devuelven resultados sin paginacion. Catalogos pequenos en la practica, pero inconsistencia con el patron global de ViewSets. | `salud/views.py:78`, `salud/views.py:90`, `salud/views.py:102`, `obra_social/views.py:43` |
| D11 | BAJA | `CORS_ALLOWED_ORIGINS = [os.getenv("SITE_URL")]` en `settings.py:192-194`: si `SITE_URL` no esta definida, la lista queda `[None]`, lo que puede causar comportamientos inesperados en CORS. | `telepark/settings.py:192-194` |
| D12 | BAJA | `ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")` -- si un host contiene comas literalmente, el split rompe el valor. Bajo impacto porque Docker siempre pasa la variable. | `telepark/settings.py:42` |

### 10.3. Estado de Salud Tecnica

| Dimension | Evaluacion |
|---|---|
| Stack y tooling | Correcto |
| Bugs de runtime | Corregido |
| Performance (N+1 mayor) | Mayormente corregido (D07 es marginal -- Evolucion no tiene FK a tabla de referencia relevante) |
| Separacion de capas | DRF desacoplado de Services |
| Codigo duplicado | Centralizado en core/ y mixins |
| Queryset estatico | Migrado a get_queryset() en ModelPKMixin |
| UnorderedObjectListWarning | Corregido (global en ViewSets + `/api/users`) |
| W001 drf-spectacular | Corregido (ModelPKMixin) |
| Rename usuarios->autenticacion | Completado |
| Paginacion global | Implementada (14 ViewSets) |
| Orden deterministico en paginacion | Implementado (BaseService + 5 overrides) |
| Opt-out catalogos | 13 ViewSets configurados via NoPaginationMixin |
| Decoradores @extend_schema_view | Centralizados via auto_tag_schema_view |
| ExceptionMiddleware | Mapeo completo de ServiceException a codigos HTTP |
| Testing | Ausente |
| Seguridad | `SECRET_KEY` expuesta (fallback en docker-compose) |
| Paginacion manual auth | Inconsistencia menor (D09) |
| APIViews sin paginar | 4 casos (D10) -- reemplazaron @action con path corregido |
| Path semantico @action | CORREGIDO (D05 resuelto en 61f41c5) |
| Password admin en stdout | CORREGIDO (16e9215) |
| CORS config | Vulnerable a `[None]` (D11) |
| Mantenibilidad | Alta -- deuda reducida significativamente |

---

## 11. Registro de Cambios Respecto al Baseline Anterior

### 11.1. Baseline HEAD (16e9215) -- Endpoints PersonaEp + MySQL 8.4

**Baseline anterior:** `cc251eb51a1095ed193d5bcde89a907f7f636c29` (refactor: correcciones de deuda tecnica)
**Baseline actual:** `16e9215222680d07ab3b520c5c20c3eedd5a47a6` (chore: upgrade MySQL 8.0 -> 8.4)

#### Commit 61f41c5 -- Endpoints PersonaEp reubicados

**Archivos Modificados:**

| Modulo | Archivos | Cambio |
|---|---|---|
| `core/` | `urls.py` | Se agregaron imports de `DiagnosticoPorPersonaEpView`, `EvolucionPorPersonaEpView`, `IndicacionPorPersonaEpView` (salud) y `OsPorPersonaEpView` (obra_social). Se agregaron 4 rutas directas bajo `/api/personaEp/{personaep_pk}/`. |
| `core/` | `mixins.py` | `auto_tag_schema_view` ahora tambien etiqueta metodos `@action` residuales (defensivo, aunque no quedan). |
| `salud/` | `views.py` | Se eliminaron 3 `@action` endpoints (`DiagnosticoViewSet.personaep`, `EvolucionViewSet.personaep`, `IndicacionViewSet.personaep`). Se agregaron 3 clases `GenericAPIView`: `DiagnosticoPorPersonaEpView`, `EvolucionPorPersonaEpView`, `IndicacionPorPersonaEpView`. Nuevos imports: `GenericAPIView`, `extend_schema`. |
| `obra_social/` | `views.py` | Se elimino 1 `@action` endpoint (`OSViewSet.personaep`). Se agrego `OsPorPersonaEpView` (GenericAPIView). Nuevos imports: `GenericAPIView`, `extend_schema`. |
| `docker-compose.yml` | `docker-compose.yml` | MySQL 8.0 -> 8.4 (incidental en este commit). |

**Commit 16e9215 -- MySQL 8.4 + Seguridad en bootstrap_admin**

| Modulo | Archivos | Cambio |
|---|---|---|
| `Dockerfile` | `Dockerfile` | Comentario de cabecera: MySQL 8.0 -> 8.4. |
| `README.md` | `README.md` | Tabla de stack: MySQL 8.0 -> 8.4. |
| `autenticacion/` | `management/commands/bootstrap_admin.py` | Se removio la impresion de la contrasena en stdout: `f'Admin...Password: {password}'` -> `'Admin creado exitosamente.'` |

#### Impacto en Metricas

| Metrica | Anterior (cc251eb) | Actual (16e9215) |
|---|---|---|
| Endpoints @action | 4 | **0** (eliminados) |
| APIViews (GenericAPIView) | 0 | **4** (agregados) |
| Total endpoints de sub-recursos | 4 (@action, path incorrecto) | 4 (APIViews, path correcto `/api/personaEp/{pk}/`) |
| ViewSets | 27 | 27 (sin cambios) |
| Services | 28 | 28 (sin cambios) |
| Serializers | 35 | 35 (sin cambios) |
| Modelos | 26 | 26 (sin cambios) |
| Dependencias externas | 0 | 0 (sin cambios) |
| Versión MySQL | 8.0 | **8.4** |
| Version Python/Django/DRF | 3.14.2/6.0.6/3.17.1 | Sin cambios |

#### Deuda Resuelta vs. Nueva en HEAD

| ID | Estado | Descripcion |
|---|---|---|
| D05 | **RESUELTO** | 4 @action con path semanticamente incorrecto (`/api/{recurso}/{pk}/personaep`). Reemplazados por APIViews con ruta correcta `/api/personaEp/{personaep_pk}/{recurso}` en commit 61f41c5. |
| D10 | **RE-CLASIFICADO** | Ya no son 4 @action sin paginacion, sino 4 APIViews sin paginacion. La inconsistencia persiste pero con implementacion distinta. |
| D13 (nuevo) | **RESUELTO** | Password de admin en stdout. Corregido en 16e9215: `bootstrap_admin.py` ya no imprime la contrasena. |
| D01..D03 | Persisten | Tests, SECRET_KEY, update_fields -- fuera de alcance. |
| D07 | Persiste | EvolucionService.filtrar_por_persona() sin select_related (ahora en EvolucionPorPersonaEpView en lugar de @action). |
| D09 | Persiste | Paginacion manual en get_users (fuera de alcance). |
| D11 | Persiste | CORS_ALLOWED_ORIGINS vulnerable a `[None]`. |
| D12 | Persiste | ALLOWED_HOSTS.split(",") fragil. |

### 11.2. Baseline cc251eb -- Correccion de Deuda Tecnica (TD-01 a TD-20)

**Resumen:** Correccion de 20 items de deuda tecnica: centralizacion de `@extend_schema_view`, eliminacion de `get_queryset()` redundante via `ModelPKMixin`, sustitucion de `pagination_class = None` por `NoPaginationMixin`, mapeo de `ServiceException` en middleware, correccion del modelo `Tipoparentesco`, saneamiento de `settings.py`, renombre `tipoEvento` -> `tipo_evento`, etc.

### 11.3. Baseline e65fbcd -- Orden Determinista en Paginacion (historico)

**Resumen:** `BaseService.listar()` ahora inyecta `order_by(PK)` automaticamente para todos los servicios. 5 servicios con FK a PersonaEp sobreescriben `listar()` con orden compuesto `(idpersonaep, PK)`.

### 11.4. Baseline 82f8202 -- Paginacion Global (historico)

**Resumen:** Se agrego `DEFAULT_PAGINATION_CLASS = PageNumberPagination` y `PAGE_SIZE = 50`. 14 ViewSets pagan automaticamente. 13 catalogos excluidos.

---

## Apendice A: Metricas de Codigo

| Metrica | Valor |
|---|---|
| Archivos Python | 70 |
| Lineas de codigo Python | ~2030 |
| Apps Django | 7 |
| Modelos | 26 |
| ViewSets | 27 |
| Endpoints @action | **0** (eliminados en 61f41c5) |
| APIViews (GenericAPIView) | **4** (agregados en 61f41c5) |
| Function views | 6 (5 auth + 1 health) |
| Services | 26 de dominio + 1 UsuarioService (static) + 1 BaseService (base) |
| Serializers | 35 |
| Excepciones de dominio | 5 + 1 base (ServiceException) |
| Mixins | 3 (ModelPKMixin, NoPaginationMixin, auto_tag_schema_view) |
| Dependencias externas | 0 (monolito modular, sin event bus ni colas) |
| Version MySQL | 8.4 (upgraded from 8.0) |

## Apendice B: Pendientes Post-Refactor

- Items D01 (tests), D02 (SECRET_KEY), D03 (update_fields) identificados como deuda estructural desde el baseline inicial y no cubiertos en ningun ciclo de refactor.
- Items D07 (Evolucion N+1), D09 (paginacion manual), D10 (APIViews sin paginar) de prioridad media/baja.
- Items D11, D12 de deteccion en escaneo cc251eb.
- Item D05 (path semantico @action) resuelto en 61f41c5.
- Item D13 (password admin en stdout) resuelto en 16e9215.
- No hay linter, formatter ni type checker configurados (fuera de alcance).
