# BASELINE — Telepark Backend

> **Propósito:** Fotografía exacta del código fuente al inicio del ciclo de refactorización Brownfield.
> **Fecha de captura:** 2026-07-02
> **Último commit:** `7c3eb7c` — "Merge branch 'develop' into 'main'"
> **Hash:** `7c3eb7c7caa4b3334e9f48848b503548c3918ebf`

---

## 1. Estructura del Proyecto

```
telepark-backend/
├── .git/
├── .specs/
│   ├── GLOBAL_RULES.md          (47 líneas) — INMUTABLE
│   ├── ESTADO.md                (archivo de estado del ciclo)
│   └── BASELINE.md              ← este archivo
├── BD/
│   └── schema.sql
├── telepark/                    (proyecto Django — configuración)
│   ├── __init__.py
│   ├── asgi.py                  (10 líneas)
│   ├── settings.py              (144 líneas)
│   ├── urls.py                  (20 líneas)
│   └── wsgi.py                  (10 líneas)
├── teleparkApi/                 (aplicación Django única)
│   ├── migrations/
│   │   ├── 0001_initial.py      (187 líneas)
│   │   ├── 0002_authgroup....py (133 líneas)
│   │   └── __init__.py          (0 líneas)
│   ├── __init__.py
│   ├── admin.py                 (1 línea) — STUB
│   ├── api.py                   (100 líneas) — ViewSets
│   ├── apps.py                  (4 líneas)
│   ├── authentication.py        (70 líneas)
│   ├── handlers.py              (41 líneas)
│   ├── helpers.py               (12 líneas)
│   ├── middleware.py            (10 líneas)
│   ├── models.py                (309 líneas) — auto-generados, managed=False
│   ├── permission.py            (5 líneas)
│   ├── serializers.py           (128 líneas)
│   ├── static.py                (5 líneas)
│   ├── tests.py                 (2 líneas) — STUB
│   ├── urls.py                  (35 líneas)
│   └── views.py                 (34 líneas) — NO ENRUTADO
├── example.env
├── manage.py                    (18 líneas)
├── package-lock.json
├── README.md
└── requirements.txt
```

**Total líneas de código (`.py`, excluyendo `__pycache__`):** 1.278 líneas

---

## 2. Dependencias Actuales (requirements.txt)

| Paquete | Versión | Estado | Recomendación |
|---------|---------|--------|---------------|
| Django | 3.2.5 | 🔴 EOL (Abril 2024) | 4.2 LTS o 5.1 |
| djangorestframework | 3.12.4 | 🟡 Desactualizado | 3.15.x |
| django-rest-swagger | 2.2.0 | 🔴 Deprecado (2019) | Reemplazar por drf-spectacular |
| django-cors-headers | 3.10.1 | 🟡 Desactualizado | 4.3.x |
| djangorestframework-simplejwt | 4.7.2 | 🟡 Desactualizado | 5.3.x |
| mysqlclient | 2.1.0 | 🟢 Estable | 2.2.x |
| python-dotenv | 0.18.0 | 🟡 Desactualizado | 1.0.x |
| PyJWT | 2.1.0 | 🔴 CVE conocido | 2.8.x+ |
| urllib3 | 1.26.6 | 🔴 CVE conocido | 2.x |
| certifi | 2021.5.30 | 🔴 Desactualizado | 2024.x+ |
| setuptools | 41.2.0 | 🔴 Obsoleto | 70.x+ |
| requests | 2.26.0 | 🟡 Desactualizado | 2.32.x |
| sqlparse | 0.4.1 | 🟡 Desactualizado | 0.5.x |
| Jinja2 | 3.0.1 | 🟡 Desactualizado | 3.1.x |
| pytz | 2021.1 | 🟡 Desactualizado | 2024.x |
| simplejson | 3.17.3 | 🟢 Estable | 3.19.x |
| MarkupSafe | 2.0.1 | 🟡 Desactualizado | 2.1.x |
| idna | 3.2 | 🟡 Desactualizado | 3.7+ |
| charset-normalizer | 2.0.4 | 🟡 Desactualizado | 3.3.x |
| asgiref | 3.4.1 | 🟡 Desactualizado | 3.8.x |
| **coreapi** | 2.3.3 | 🔴 Muerta (transitiva swagger) | Eliminar |
| **coreschema** | 0.0.4 | 🔴 Muerta (transitiva swagger) | Eliminar |
| **openapi-codec** | 1.3.2 | 🔴 Muerta (transitiva swagger) | Eliminar |
| **uritemplate** | 3.0.1 | 🔴 Muerta (transitiva swagger) | Eliminar |
| **itypes** | 1.2.0 | 🔴 Muerta (transitiva swagger) | Eliminar |

**Dependencias funcionales directas:** Django, djangorestframework, django-cors-headers, djangorestframework-simplejwt, mysqlclient, python-dotenv  
**Dependencias funcionales transitivas:** PyJWT, urllib3, certifi, requests, sqlparse, Jinja2, pytz, simplejson, MarkupSafe, idna, charset-normalizer, asgiref, setuptools  
**Dependencias MUERTAS (eliminables sin impacto):** django-rest-swagger, coreapi, coreschema, openapi-codec, uritemplate, itypes

---

## 3. Endpoints Activos (enrutados en urls.py)

### Endpoints directos:
| Método | Ruta | Función | Autenticación |
|--------|------|---------|---------------|
| POST | `/api/login` | `auth_view` | Pública |
| POST | `/api/create_user` | `create_user` | IsSuperuser |
| POST | `/api/refresh_token` | `TokenRefreshView` | Pública |
| GET | `/api/users` | `get_users` | IsSuperuser |
| PUT | `/api/update_user` | `update_user` | IsSuperuser |

### Endpoints registrados vía DefaultRouter (ViewSets):
| ViewSet | Rutas generadas (CRUD) | Modelo |
|---------|----------------------|--------|
| PersonaViewSet | GET/POST `/api/persona`, GET/PUT/DELETE `/api/persona/{pk}` | Persona |
| PersonaEPViewSet | GET/POST `/api/personaEp`, GET/PUT/DELETE `/api/personaEp/{pk}` | PersonaEp |
| PersonaPViewSet | GET/POST `/api/personaP`, GET/PUT/DELETE `/api/personaP/{pk}` | PersonaEp |
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

**Total endpoints activos: ~80+** (considerando CRUD completo x 16 ViewSets + 5 directos + 4 acciones personalizadas)

---

## 4. Hallazgos de Código Muerto (Dead Code)

### 4.1. `teleparkApi/views.py` (34 líneas — 100% muerto)
Archivo completo con funciones `@api_view` que **no están registradas en ningún `urls.py`**:
- `persona_list` (POST/GET)
- `direccion_list` (POST)
- `personaEp_list` (POST)
- `tipoParentesco_list` (POST)
- `localidad_list` (GET)
- `municipio_list` (GET) — definido DOS VECES (líneas 34 y 40)

**Origen:** Código legacy reemplazado por ViewSets en `api.py`. Nunca se eliminó.

### 4.2. `teleparkApi/admin.py` (1 línea)
Solo importa `django.contrib.admin`. Sin registros de modelos. Stub.

### 4.3. `teleparkApi/tests.py` (2 líneas)
Solo importa `TestCase`. Sin tests. Stub.

### 4.4. `teleparkApi/serializers.py` — Serializador duplicado
`EnfermedadSerializer` definido **dos veces** (líneas 11-14 y 45-48) — contenido idéntico.

### 4.5. `django-rest-swagger` y dependencias transitivas
El paquete `django-rest-swagger==2.2.0` no está importado en ningún archivo `.py`. Arrastra 5 dependencias muertas: `coreapi`, `coreschema`, `openapi-codec`, `uritemplate`, `itypes`.

---

## 5. Bugs Detectados (No funcionales — preexistente)

| Bug | Archivo | Descripción |
|-----|---------|-------------|
| B001 | `teleparkApi/urls.py:17` | `PersonaPViewSet` y `PersonaEPViewSet` comparten `basename='personaEp'` → colisión de nombres de ruta |
| B002 | `teleparkApi/serializers.py:100` | `tipoEvento = TipoEventoSerializer` (asignación de clase, no instancia) → no serializa nested object |
| B003 | `telepark/urls.py:21` | `re_path(r'^', include('teleparkApi.urls'))` captura TODAS las rutas, incluyendo `/admin/` |

---

## 6. Firma de Seguridad Inicial

| Aspecto | Estado | Nota |
|---------|--------|------|
| SECRET_KEY hardcodeada | 🔴 Inseguro | En settings.py línea 40 |
| ALLOWED_HOSTS = ['*'] | 🔴 Inseguro | En settings.py línea 45 |
| DEBUG en env variable | 🟢 Aceptable | `os.getenv("ENV") == 'dev'` |
| CSRF_TRUSTED_ORIGINS | 🟡 Mejorable | Desde env pero sin fallback |
| JWT sin blacklist | 🟡 Mejorable | `BLACKLIST_AFTER_ROTATION: True` pero sin backend |
| TLS no configurado | 🟡 Pendiente | Depende del proxy |
| Versión Django EOL | 🔴 Crítico | No recibe parches de seguridad |
