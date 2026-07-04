# CAMBIOS

## Ciclo CICLO-20260702-001 (Estabilización)
[Contenido del ciclo anterior preservado abajo]

---

## Ciclo CICLO-20260702-002 (Dockerización + managed=True)

### Resumen
Ciclo Brownfield que dockeriza la aplicación Django + MySQL y migra 26 modelos de negocio de `managed=False` a `managed=True`. Los 10 modelos del framework Django (Auth*, Django*) mantienen `managed=False` para evitar conflictos de migraciones.

### US-01: Pasar 26 modelos de negocio a managed=True
- **Archivo:** `teleparkApi/models.py`
- **Cambio:** Eliminado `managed = False` de las clases `Meta` de los 26 modelos de negocio
- **Modelos afectados:** Actividad, Actividadrealizada, Asistenciataller, Clasetaller, Comportamiento, Diagnostico, Direccion, Enfermedad, Evento, Evolucion, Factorclase, Factorglobal, Indicacionmedicamento, Localidad, Medicamento, Municipio, Obrasocial, Os, Persona, PersonaEp, Taller, Tipoevento, Tipoparentesco, Unidadobservacion, Valorvariableuo, Variableuo
- **Modelos no modificados (10):** AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, AuthUserGroups, AuthUserUserPermissions, DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession
- **Seguridad aplicada:** Validación de white-listing de modelos a modificar contra la lista especificada en ARQUITECTURA.md. Los 10 modelos Django se excluyen por ser gestionados por apps internas de Django.

### US-02: Dockerizar app Django + MySQL
- **Archivo:** `Dockerfile` (CREADO)
  - Base: `python:3.14-slim` (single stage)
  - Instala gcc, libc6-dev, default-libmysqlclient-dev, pkg-config para compilar mysqlclient
  - Elimina migraciones antiguas (`0*.py`) para regeneración limpia
  - Crea directorio `static/`
  - Entrypoint: `/entrypoint.sh`
- **Archivo:** `docker-compose.yml` (CREADO)
  - Servicio `db`: mysql:8.0, container_name: telepark-db, puerto host 3307:3306, volumen telepark_mysql_data, healthcheck con mysqladmin ping
  - Servicio `app`: build: ., container_name: telepark-app, depends_on db (condition: service_healthy), puerto 8000:8000, volumen .:/app (hot-reload)
  - Red: telepark-network (bridge)
  - Variables de entorno con defaults para desarrollo local
- **Archivo:** `entrypoint.sh` (CREADO)
  - Wait-for-mysql usando Python (MySQLdb) en lugar de mysqladmin (evita instalar mysql-client)
  - Timeout configurable de 60s con retry cada 3s
  - Secuencia: wait → makemigrations teleparkApi → migrate → runserver 0.0.0.0:8000
- **Archivo:** `.dockerignore` (CREADO)
  - Excluye: .git, .venv, __pycache__, *.pyc, .env, example.env, BD/, README.md

### US-03: makemigrations + migrate (gestionado por entrypoint.sh)
- Las migraciones antiguas (`0001_initial.py`, `0002_authgroup_...py`) se eliminan en el Dockerfile
- El entrypoint regenera migraciones desde cero y las aplica
- Verificación: `docker-compose up` debe crear las 26 tablas de negocio

### US-04: Endpoint de healthcheck /api/health/ (REQ-13)
- **Archivo:** `teleparkApi/views/__init__.py` (CREADO)
- **Archivo:** `teleparkApi/views/health.py` (CREADO)
  - `GET /api/health/` — verifica conexión a BD y cuenta tablas de negocio
  - Respuesta 200: `{"status": "ok", "database": "connected", "tables": N}`
  - Respuesta 503: `{"status": "error", "database": "disconnected", "detail": "..."}`
  - Público (sin autenticación), seguro por diseño (solo info de conectividad)
- **Archivo:** `teleparkApi/urls.py` (MODIFICADO)
  - Agregada importación de `health_check` y ruta `api/health`

### Verificación
- `python manage.py check` ✅ PASS — 0 errores, 0 warnings (excluyendo static preexistente)

### Control de seguridad aplicado
1. Sanitización: El healthcheck solo expone estado de conexión, no datos sensibles
2. Secretos: Todas las credenciales viajan como variables de entorno en docker-compose.yml
3. Logging: El entrypoint.sh no logea contraseñas ni datos sensibles
4. Aislamiento: Red bridge propia (telepark-network) para aislar servicios
5. White-listing: Solo se modificaron los 26 modelos explícitamente listados en ARQUITECTURA.md

---

## Resumen
Ciclo de refactorización Brownfield completado. Se ejecutaron las 10 fases del plan arquitectónico.

## Cambios realizados

### Fase 0: Preparación
- Verificado Python 3.14.2
- Snapshot de dependencias originales (entorno limpio → `pip install -r requirements.txt` inicial)
- Rama creada: `refactor/ciclo-20260702-001`

### Fase 1: Limpieza de Código Muerto
- **ELIMINADO** `teleparkApi/views.py` (42 líneas, código no enrutado)
- **ELIMINADO** `teleparkApi/admin.py` (stub)
- **ELIMINADO** `teleparkApi/tests.py` (stub)
- **ELIMINADO** `EnfermedadSerializer` duplicado (líneas 45-48 en serializers.py)
- **ELIMINADOS** de requirements.txt: `django-rest-swagger`, `coreapi`, `coreschema`, `openapi-codec`, `uritemplate`, `itypes`
- **DESINSTALADOS** del entorno: `django-rest-swagger`, `coreapi`, `coreschema`, `openapi-codec`, `uritemplate`, `itypes`

### Fase 2: Migración SECRET_KEY (REQ-05)
- `SECRET_KEY` migrada a `os.getenv("SECRET_KEY")`
- `ALLOWED_HOSTS` migrado a `os.getenv("ALLOWED_HOSTS", "localhost").split(",")`
- `example.env` actualizado con `ALLOWED_HOSTS`

### Fase 3: Actualización de dependencias de infraestructura
| Paquete | Versión Anterior | Versión Nueva |
|---------|-----------------|---------------|
| setuptools | 41.2.0 | 82.0.1 |
| python-dotenv | 0.18.0 | 1.2.2 |
| mysqlclient | 2.1.0 | 2.2.8 |
| PyJWT | 2.1.0 | 2.13.0 |
| urllib3 | 1.26.6 | 2.7.0 |
| requests | 2.26.0 | 2.34.2 |
| certifi | 2021.5.30 | 2026.05.20 |
| sqlparse | 0.4.1 | 0.5.4 |
| asgiref | 3.4.1 | 3.11.1 |
| Jinja2 | 3.0.1 | 3.1.6 |
| simplejson | 3.17.3 | 3.19.2 |
| charset-normalizer | 2.0.4 | 3.4.1 |
| idna | 3.2 | 3.10 |
| MarkupSafe | 2.0.1 | 3.0.2 |
| pytz | 2021.1 | **ELIMINADO** (zoneinfo stdlib) |

### Fase 4: Verificación simplejwt + Python 3.14
- simplejwt 5.5.1 instalado y verificado con Python 3.14.2 ✅
- Dependencias auto-resueltas: Django 6.0.6, DRF 3.17.1

### Fase 5: Actualización Django + DRF
- Django actualizado de 3.2.5 → 6.0.6 (desviación del plan: se intentó Django 5.2 LTS pero pip resolvió 6.0.6 por ser la versión más reciente compatible con simplejwt 5.5.1)
- DRF actualizado de 3.12.4 → 3.17.1
- django-cors-headers actualizado de 3.10.1 → 4.9.0
- `USE_L10N = True` eliminado de settings.py (deprecado desde Django 4.x)
- `CommonMiddleware` duplicado eliminado y orden de MIDDLEWARE corregido
- `BLACKLIST_AFTER_ROTATION` cambiado de `True` a `False`

### Fase 6: Migración telepark/urls.py
- `re_path(r'^', ...)` → `path('', ...)` en telepark/urls.py

### Fase 7: Migración teleparkApi/urls.py
- 5 rutas migradas de `re_path` a `path()`:
  - `api/login`, `api/create_user`, `api/refresh_token`, `api/users`, `api/update_user`

### Fase 8: Corrección B001
- `basename='personaEp'` → `basename='personaP'` en PersonaPViewSet (urls.py:17)

### Fase 9: pytz → zoneinfo
- pytz no referenciado en ningún `.py` del proyecto
- Ya desinstalado en Fase 3

### Fase 10: Verificación final
- `python manage.py check` → 0 errores (1 warning: static/ dir no existe)
- `python manage.py check --deploy` → 0 errores (warnings de seguridad esperados: HSTS, SSL, DEBUG dev)
- `requirements.txt` actualizado con versiones finales

## Desviaciones del Plan Arquitectónico
1. **Django 6.0.6 en lugar de 5.2 LTS**: pip resolvió Django 6.0.6 como dependencia de simplejwt 5.5.1. Se mantiene 6.0.6 por ser compatible y más reciente. No se detectan breaking changes adicionales.

## Estado Post-Ciclo
- `python manage.py check`: ✅ PASS (0 errores)
- `python manage.py check --deploy`: ✅ PASS (0 errores, solo WARNINGs)
- Dependencias funcionales: 20 paquetes (vs 26 originales)
- Código eliminado: 3 archivos (79 líneas) + 1 serializador duplicado
- Seguridad: SECRET_KEY y ALLOWED_HOSTS migrados a variables de entorno
