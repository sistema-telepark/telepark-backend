# ARQUITECTURA — Contrato Arquitectónico de Estabilización

> **Ciclo:** CICLO-20260702-001  
> **Fecha:** 2026-07-02  
> **Modo:** BROWNFIELD  
> **Artefacto:** Contrato vinculante para el plan de estabilización del entorno  
> **Precedencia:** Este documento tiene precedencia sobre decisiones técnicas ad-hoc. Solo puede ser modificado mediante aprobación explícita del orquestador.

---

## Índice

1. [Orden de Ejecución (Roadmap en Fases)](#1-orden-de-ejecución-roadmap-en-fases)
2. [Estrategia de Rollback](#2-estrategia-de-rollback)
3. [SECRET_KEY y settings.py](#3-secret_key-y-settingspy)
4. [pytz → zoneinfo](#4-pytz--zoneinfo)
5. [Verificación de compatibilidad simplejwt + Python 3.14](#5-verificación-de-compatibilidad-simplejwt--python-314)
6. [Análisis de Breaking Changes](#6-análisis-de-breaking-changes)
7. [Diagrama de Arquitectura Post-Estabilización](#7-diagrama-de-arquitectura-post-estabilización)
8. [Matriz de Riesgos](#8-matriz-de-riesgos)
9. [Contrato Vinculante](#9-contrato-vinculante)
10. [Aprobación](#10-aprobación)

---

## 1. Orden de Ejecución (Roadmap en Fases)

El orden propuesto minimiza superficie de error al **eliminar dead code y dependencias muertas primero**, antes de tocar cualquier actualización de paquetes. Esto reduce las variables en juego durante la actualización de Django/DRF.

### Fase 0: Preparación y Snapshot

| # | Acción | Comando / Detalle | Justificación |
|---|--------|-------------------|---------------|
| 0.1 | Verificar Python 3.14.2 | `python --version` | Precondición: el intérprete debe ser 3.14.2 |
| 0.2 | Snapshot de dependencias actuales | `pip freeze > .specs/requirements-baseline.txt` | Línea base para rollback de pip |
| 0.3 | Snapshot de git | `git stash push -m "PRE-REFACTOR-$(date +%Y%m%d)"` (opcional) | Preservar cambios no commiteados |
| 0.4 | Verificar git status limpio | `git status` | Asegurar que partimos del commit `7c3eb7c` |
| 0.5 | Crear rama de trabajo | `git checkout -b refactor/ciclo-20260702-001` | Aislar cambios |

### Fase 1: Limpieza de Código Muerto (US-02, US-03)

| # | Archivo | Acción | Comando / Detalle |
|---|---------|--------|-------------------|
| 1.1 | `teleparkApi/views.py` | **ELIMINAR** archivo completo (42 líneas, 100% no enrutado) | `git rm teleparkApi/views.py` |
| 1.2 | `teleparkApi/admin.py` | **ELIMINAR** archivo (stub sin registros) | `git rm teleparkApi/admin.py` |
| 1.3 | `teleparkApi/tests.py` | **ELIMINAR** archivo (stub sin tests) | `git rm teleparkApi/tests.py` |
| 1.4 | `teleparkApi/serializers.py` | **ELIMINAR** duplicado `EnfermedadSerializer` (líneas 45-48) | Eliminar segunda definición (conservar líneas 11-14) |
| 1.5 | Remover dependencias muertas de `requirements.txt` | **ELIMINAR** 6 líneas: `django-rest-swagger`, `coreapi`, `coreschema`, `openapi-codec`, `uritemplate`, `itypes` | Editar `requirements.txt` |
| 1.6 | Verificar imports no rotos | `python -c "import teleparkApi"` o `python manage.py check` | Confirmar que nada importaba estos módulos |

**Criterio de éxito Fase 1:** `python manage.py check` debe ejecutarse sin errores de importación.

### Fase 2: Migración de SECRET_KEY a variable de entorno (REQ-05)

| # | Acción | Detalle |
|---|--------|---------|
| 2.1 | En `settings.py`: reemplazar `SECRET_KEY = 'django-insecure-...'` por `SECRET_KEY = os.getenv("SECRET_KEY")` | Acepta el valor desde `.env` |
| 2.2 | En `settings.py`: reemplazar `ALLOWED_HOSTS = ['*']` por `ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")` | Restringir hosts |
| 2.3 | Verificar que `example.env` ya contiene `SECRET_KEY=` (línea 8) | Ya existe — solo asegurar visibilidad en README/docs |
| 2.4 | Verificar `CSRF_TRUSTED_ORIGINS` de lista unitaria | Actualmente `[os.getenv("CSRF_TRUSTED_ORIGINS")]` — OK para este ciclo |

**Criterio de éxito Fase 2:** `python manage.py check --deploy` reporta CERO errores de seguridad críticos.

### Fase 3: actualizar dependencias de infraestructura (no Django)

Actualizar paquetes que NO son Django/DRF primero, para aislar problemas.

| # | Paquete | Versión objetivo | Comando |
|---|---------|-----------------|---------|
| 3.1 | setuptools | 82.0.1 | `pip install setuptools==82.0.1` |
| 3.2 | python-dotenv | 1.2.2 | `pip install python-dotenv==1.2.2` |
| 3.3 | mysqlclient | 2.2.8 | `pip install mysqlclient==2.2.8` |
| 3.4 | PyJWT | 2.13.0 | `pip install PyJWT==2.13.0` |
| 3.5 | urllib3 | 2.7.0 | `pip install urllib3==2.7.0` |
| 3.6 | requests | 2.34.2 | `pip install requests==2.34.2` |
| 3.7 | certifi | 2026.05.20 | `pip install certifi==2026.05.20` |
| 3.8 | sqlparse | 0.5.4 | `pip install sqlparse==0.5.4` |
| 3.9 | asgiref | 3.11.1 | `pip install asgiref==3.11.1` |
| 3.10 | Jinja2 | 3.1.6 | `pip install Jinja2==3.1.6` |
| 3.11 | simplejson | 3.19.x (última compatible) | `pip install simplejson==3.19.x` |
| 3.12 | MarkupSafe | junto con Jinja2 | se actualiza automáticamente |
| 3.13 | charset-normalizer | junto con requests | se actualiza automáticamente |
| 3.14 | idna | junto con requests | se actualiza automáticamente |
| 3.15 | pytz | **ELIMINAR** | `pip uninstall pytz -y` |

**Criterio de éxito Fase 3:** `pip freeze` muestra todas las versiones objetivo. `python manage.py check` sin errores.

### Fase 4: Verificar simplejwt + Python 3.14 (pre-actualización Django)

**Ver sección 5** — esta fase es un checkpoint previo a la actualización de Django.

- Instalar simplejwt 5.5.1 de forma aislada
- Probar importación y configuración básica
- Si falla → ejecutar plan de contingencia (sección 5.2)

### Fase 5: Actualizar Django + DRF + dependencias asociadas

| # | Acción | Comando | Notas |
|---|--------|---------|-------|
| 5.1 | Instalar Django 5.2 LTS | `pip install Django==5.2` | Puede resolver sqlparse, asgiref automáticamente |
| 5.2 | Modificar `settings.py` para Django 5.2 | Ver sección 3 | `DEFAULT_AUTO_FIELD`, `MIDDLEWARE`, etc. |
| 5.3 | Instalar DRF 3.17.1 | `pip install djangorestframework==3.17.1` | Soporta Django 4.2-6.0 |
| 5.4 | Instalar simplejwt 5.5.1 | `pip install djangorestframework-simplejwt==5.5.1` | Requiere DRF ≥3.14 |
| 5.5 | Instalar django-cors-headers 4.9.0 | `pip install django-cors-headers==4.9.0` | Compatible Django 4.2-6.0 |
| 5.6 | Ejecutar `python manage.py check` | Verificar sin errores | |
| 5.7 | Ejecutar `python manage.py check --deploy` | Verificar REQ-05 | |

### Fase 6: Actualizar `telepark/urls.py` — `re_path` → `path` (REQ-13, B003)

| # | Acción | Detalle |
|---|--------|---------|
| 6.1 | Reemplazar `re_path(r'^', include('teleparkApi.urls'))` por `path('', include('teleparkApi.urls'))` | No requiere regex. Django 5.2 acepta `path` con string vacío como raíz |

**Nota:** El bug B003 (`re_path(r'^', ...)` captura todo incluyendo `/admin/`) **NO se corrige** funcionalmente — solo se migra la sintaxis a `path()` que es semánticamente equivalente. La corrección del bug (orden de urlpatterns) queda fuera de alcance.

### Fase 7: Actualizar `teleparkApi/urls.py` — `re_path` → `path`

| # | Ruta actual (`re_path`) | Ruta nueva (`path`) |
|---|------------------------|---------------------|
| 7.1 | `re_path(r'^api/login$', ...)` | `path('api/login', ...)` |
| 7.2 | `re_path(r'^api/create_user$', ...)` | `path('api/create_user', ...)` |
| 7.3 | `re_path(r'^api/users$', ...)` | `path('api/users', ...)` |
| 7.4 | `re_path(r'^api/update_user$', ...)` | `path('api/update_user', ...)` |
| 7.5 | `re_path('api/refresh_token', ...)` | `path('api/refresh_token', ...)` (mantener name='token_refresh') |

**Importante:** En Django 5.2, `re_path` NO está obsoleto, pero se migra a `path` por claridad y consistencia. Las rutas exactas (`$`) se convierten a `path()` sin el `$` — Django 5.2 trata `path('api/login', ...)` como coincidencia exacta por defecto (no se requiere `$`).

### Fase 8: Corrección de B001 (basename duplicado — REQ-13)

| # | Acción | Archivo: línea | Cambio |
|---|--------|---------------|--------|
| 8.1 | Cambiar basename de `PersonaPViewSet` | `teleparkApi/urls.py:17` | `basename = 'personaEp'` → `basename = 'personaP'` |

**Justificación:** REQ-13 exige corrección si B001 causa conflicto post-actualización. Django 5.2 + DRF 3.17 rechazan `basename` duplicados con error explícito en `check`. Es sintácticamente inválido.

### Fase 9: `pytz` → `zoneinfo` (settings.py)

**Ver sección 4.**

### Fase 10: Verificación final y freeze

| # | Acción | Comando |
|---|--------|---------|
| 10.1 | Compilación | `python manage.py check` |
| 10.2 | Seguridad | `python manage.py check --deploy` |
| 10.3 | Freeze final | `pip freeze > requirements.txt` |
| 10.4 | Commit | `git add -A && git commit -m "[CICLO-20260702-001] Estabilización de entorno - Fase completa"` |

---

## 2. Estrategia de Rollback

### 2.1. Rollback por Fase

Cada fase es autocontenida y reversible mediante `git revert` del commit correspondiente.

| Fase | Estrategia de revert | Comando |
|------|---------------------|---------|
| Fase 1 (dead code) | `git revert <commit>` o `git checkout baseline -- <files>` | Restaurar archivos eliminados y dependencias muertas |
| Fase 2 (SECRET_KEY) | `git revert <commit>` | Volver a SECRET_KEY hardcodeada |
| Fase 3 (deps infra) | `pip install -r .specs/requirements-baseline.txt` | Reinstalar versiones originales |
| Fase 4 (simplejwt test) | `pip install djangorestframework-simplejwt==4.7.2` | Volver a versión anterior |
| Fase 5 (Django+DRF) | `pip install -r .specs/requirements-baseline.txt` | Revertir todo el requirements |
| Fase 6-8 (urls) | `git revert <commit>` | Restaurar urlpatterns originales |
| Fase 9 (zoneinfo) | `git revert <commit>`; `pip install pytz==2021.1` | Restaurar pytz |

### 2.2. Rollback Total

```bash
# Si todo falla:
git checkout -- .                        # Descartar cambios locales
git stash drop                           # (si se hizo stash)
pip install -r .specs/requirements-baseline.txt  # Reinstalar dependencias originales
```

### 2.3. Snapshot de Seguridad

Antes de cada `pip install` que actualice un paquete mayor, ejecutar:

```bash
pip freeze > .specs/requirements-punto-control-{FASE}.txt
```

---

## 3. SECRET_KEY y settings.py

### 3.1. Migración de SECRET_KEY (REQ-05)

**Estado actual:** `settings.py:40` — hardcodeada: `SECRET_KEY = 'django-insecure-5@j$75afof+#p%ft9d4e!)x7%_8na_3arrrb19k1enrjz*g+%u'`

**Estado objetivo:**

```python
SECRET_KEY = os.getenv("SECRET_KEY")
```

**Archivo `example.env`** ya contiene `SECRET_KEY=` (línea 8). Se requiere solo asegurar que la documentación del proyecto indique que esta variable es obligatoria.

**Verificación:** `python manage.py check --deploy` no debe listar `SECRET_KEY` como error.

### 3.2. ALLOWED_HOSTS

**Estado actual:** `ALLOWED_HOSTS = ['*']` (settings.py:45)

**Estado objetivo:**

```python
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
```

Agregar al `example.env`:
```
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3.3. DEFAULT_AUTO_FIELD

**Estado actual:** `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` (settings.py:187)

**Análisis:** Desde Django 3.2+, `BigAutoField` es el valor por defecto implícito. En Django 5.2, sigue siendo el valor por defecto. **No requiere cambio.** Se mantiene explícito por claridad.

### 3.4. MIDDLEWARE

**Estado actual** (settings.py:62-73):

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',       # DUPLICADO!
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'teleparkApi.middleware.ExceptionMiddleware',
]
```

**Problemas detectados:**
1. `CommonMiddleware` aparece **dos veces** (líneas 64 y 68) — `SessionMiddleware` debería ir antes de `CommonMiddleware` según la documentación de Django. Se elimina el duplicado.
2. Orden correcto recomendado por Django 5.2: Security → Session → Common → Csrf → Auth → Messages → Clickjacking

**Estado objetivo:**

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'teleparkApi.middleware.ExceptionMiddleware',
]
```

**Justificación:** Se eliminó `CommonMiddleware` duplicado. Se movió `SessionMiddleware` antes de `CommonMiddleware` (orden estándar Django). `CorsMiddleware` se mantiene primero (requisito de django-cors-headers).

### 3.5. USE_L10N

**Análisis:** `USE_L10N = True` (settings.py:174) está **deprecado** desde Django 4.x y eliminado en Django 5.x. Causará `RemovedInDjango50Warning` o error directo.

**Acción:** **ELIMINAR** `USE_L10N = True` de `settings.py`. Django 5.2 usa `USE_I18N` y formateo por defecto habilitado.

### 3.6. Cambios adicionales en settings.py

| Aspecto | Cambio | Razón |
|---------|--------|-------|
| `USE_L10N` | ELIMINAR | Deprecado desde Django 4.0, eliminado en 5.0 |
| `MIDDLEWARE` | Reordenar y eliminar duplicado | Ver sección 3.4 |
| `SECRET_KEY` | `os.getenv("SECRET_KEY")` | Cumplir REQ-05 |
| `ALLOWED_HOSTS` | `os.getenv("ALLOWED_HOSTS", "localhost").split(",")` | Cumplir REQ-05 |

---

## 4. pytz → zoneinfo

### 4.1. Contexto

- Python 3.9+ incluye `zoneinfo` en la stdlib
- Django 5.2+ usa `zoneinfo` por defecto (desde Django 4.0)
- `pytz` actualmente listado en `requirements.txt` como dependencia directa
- `USE_TZ = True` ya está en settings.py

### 4.2. Estrategia

| # | Acción | Detalle |
|---|--------|---------|
| 1 | Verificar que `pytz` no se importa en ningún `.py` del proyecto | `grep -r "import pytz" .` y `grep -r "from pytz" .` deben dar vacío |
| 2 | Eliminar `pytz` de `requirements.txt` | Remover línea `pytz==2021.1` |
| 3 | Ejecutar `pip uninstall pytz -y` | Remover del entorno |
| 4 | Verificar que `settings.py` no menciona `pytz` | No hay mención actual |

### 4.3. Cambios en settings.py

**No se requieren cambios.** `USE_TZ = True` y `TIME_ZONE = 'UTC'` son compatibles con Django 5.2 y `zoneinfo`. Django 5.2 detecta automáticamente `zoneinfo` disponible y lo usa en lugar de `pytz`.

**Verificación:** `python manage.py check` no debe reportar errores relacionados con timezone.

### 4.4. Riesgo potencial

Si algún modelo usa campos `DateTimeField` con `pytz` específico (ej. `pytz.timezone('America/Argentina/Buenos_Aires')`), requeriría migración a `zoneinfo.ZoneInfo`. No se ha detectado este patrón en el código actual.

---

## 5. Verificación de compatibilidad simplejwt + Python 3.14

### 5.1. Plan de Verificación

simplejwt 5.5.1 declara oficialmente soporte para Python 3.9-3.13. Python 3.14 no está en su matriz de pruebas. Se requiere verificación empírica.

**Checkpoint obligatorio** antes de Fase 5:

```bash
# Paso 1: Instalar simplejwt 5.5.1 de forma aislada en un entorno limpio
# (O en el entorno actual si no hay conflictos)
pip install djangorestframework-simplejwt==5.5.1 djangorestframework==3.17.1

# Paso 2: Verificar que importa correctamente
python -c "
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
print('simplejwt OK - imports exitosos')
print(f'Python: {__import__(\"sys\").version}')
print(f'simplejwt: {api_settings.ACCESS_TOKEN_LIFETIME}')
"

# Paso 3: Verificar que Django 5.2 arranca con simplejwt
python manage.py check

# Paso 4: Probar endpoint de login real
python manage.py shell -c "
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Verificar que la creación de tokens funciona
user = User.objects.first()  # asumiendo que hay al menos un usuario
if user:
    token = RefreshToken.for_user(user)
    print(f'Access: {str(token.access_token)[:20]}...')
    print('Token generation OK')
"
```

### 5.2. Plan de Contingencia (si simplejwt 5.5.1 falla en Python 3.14)

| Escenario | Acción | Alternativa |
|-----------|--------|-------------|
| simplejwt 5.5.1 no instala | Reportar a upstream, esperar parche | Usar PyJWT 2.13.0 directamente con implementación custom |
| simplejwt 5.5.1 instala pero falla en runtime | Degradar a simplejwt 5.4.x (última versión pre-5.5) | Probar compatibilidad parcial |
| simplejwt 5.4.x también falla | Implementar JWT manual con PyJWT 2.13.0 | No recomendado para este ciclo |

**Decisión vinculante:** Si simplejwt falla en Python 3.14, **no se retrasa el ciclo**. Se procede con implementación JWT usando PyJWT 2.13.0 directamente, replicando la interfaz mínima necesaria. Esto queda registrado en `CAMBIOS.md`.

---

## 6. Análisis de Breaking Changes

### 6.1. Django 3.2 → 5.2 LTS

| Cambio | Impacto | Acción Requerida |
|--------|---------|------------------|
| `DEFAULT_AUTO_FIELD` ahora es `BigAutoField` por defecto | Ninguno (ya está explícito) | Ninguna |
| `USE_L10N` eliminado | **ALTO** — causa error en settings.py | Eliminar línea `USE_L10N = True` |
| `MIDDLEWARE` — orden más estricto | **BAJO** — Django 5.2 es menos tolerante a middleware duplicado | Corregir duplicado de `CommonMiddleware` |
| `urlpatterns` — `path()` recomendado sobre `re_path()` | **MEDIO** — `re_path` sigue funcionando pero se migra por claridad | Migrar a `path()` (Fases 6-7) |
| `urlpatterns` — `re_path` con `r'^'` y `include()` | **BAJO** — sigue funcionando pero se migra a `path('', include(...))` | Migrar en Fase 6 |
| `settings.py` — `CSRF_TRUSTED_ORIGINS` requiere lista | **BAJO** — ya es lista | Ninguna |
| `TEMPLATES` — `APP_DIRS: True` es compatible | Ninguno | Ninguna |
| `AUTH_PASSWORD_VALIDATORS` — sin cambios | Ninguno | Ninguna |
| `REST_FRAMEWORK` dict — compatible | Ninguno | Ninguna |
| `SIMPLE_JWT` dict — compatible | **MEDIO** — simplejwt 5.5.1 cambia claves de configuración | Ver sección 6.3 |
| Remoción de `pytz` como dependencia de Django | Ninguno | Django 5.2 usa `zoneinfo` de stdlib |

### 6.2. DRF 3.12 → 3.17.1

| Cambio | Impacto | Acción Requerida |
|--------|---------|------------------|
| `ViewSets` — sin cambios en API pública | Ninguno | Ninguna |
| `@action(detail=True)` — compatible | Ninguno | Ninguna |
| `ModelViewSet` — compatible | Ninguno | Ninguna |
| `DefaultRouter` — compatible | Ninguno | Ninguna |
| `serializers.ModelSerializer` — sin cambios | Ninguno | Ninguna |
| `JSONParser` — compatible | Ninguno | Ninguna |
| `JsonResponse` — compatible | Ninguno | Ninguna |
| drf-yasg / swagger: no aplica | N/A | django-rest-swagger ya eliminado |

### 6.3. simplejwt 4.7 → 5.5.1

| Cambio | Impacto | Acción Requerida |
|--------|---------|------------------|
| `BLACKLIST_AFTER_ROTATION` requiere backend de blacklist | **MEDIO** — actualmente `True` sin backend | Cambiar a `False` o instalar backend. Para este ciclo, se cambia a `False` |
| `ROTATE_REFRESH_TOKENS` — compatible | Ninguno | Ninguna |
| `AUTH_TOKEN_CLASSES` — compatible | Ninguno | Ninguna |
| `USER_ID_FIELD: 'username'` — compatible | Ninguno | Validar que el campo `username` existe en `auth_user` |
| Configuración de `SIMPLE_JWT` dict — estructura compatible | Ninguno | Ninguna |

**Decisión:** `BLACKLIST_AFTER_ROTATION` se cambia de `True` a `False` porque simplejwt 5.x requiere un backend de blacklist explícito (ej. `rest_framework_simplejwt.token_blacklist`) que no está instalado ni se va a instalar en este ciclo.

### 6.4. urllib3 1.26 → 2.7.0

| Cambio | Impacto | Acción Requerida |
|--------|---------|------------------|
| API de pooling reescrita | **BAJO** — requests 2.34.2 encapsula urllib3 | Actualizar requests junto con urllib3 |
| Solo HTTP/2 (eliminado HTTP/1.1 puro) | **BAJO** — requests 2.34.2 maneja la transición | Ninguna |
| OpenSSL ≥1.1.1 requerido | **BAJO** — Python 3.14 incluye OpenSSL 3.x | Verificar con `python -c "import ssl; print(ssl.OPENSSL_VERSION)"` |
| Eliminación de `urllib3.util.retry.Retry` | **BAJO** — no usado en el proyecto | Ninguna |

### 6.5. python-dotenv 0.18 → 1.2.2

| Cambio | Impacto | Acción Requerida |
|--------|---------|------------------|
| `set_key()` / `unset_key()` — firma modificada | **BAJO** — no se usan en el proyecto | Ninguna |
| `load_dotenv()` — compatible | Ninguno | Ninguna |
| `find_dotenv()` — compatible | Ninguno | Ninguna |

---

## 7. Diagrama de Arquitectura Post-Estabilización

### 7.1. Visión General

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          TELEPARK BACKEND                                │
│              Entorno Estabilizado — Django 5.2 LTS + DRF 3.17.1          │
└──────────────────────────────────────────────────────────────────────────┘

┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   Cliente    │────▶│   Nginx/Proxy    │────▶│  Gunicorn/ASGI   │
│  (Web/Mobile)│     │  (TLS terminator)│     │  (WSGI/ASGI)     │
└──────────────┘     └──────────────────┘     └──────────────────┘
                                                      │
                                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          DJANGO 5.2 LTS                                  │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │  MIDDLEWARE (9 capas)                                              │  │
│  │  CorsMiddleware → Security → Session → Common → CSRF → Auth →    │  │
│  │  Messages → XFrameOptions → ExceptionMiddleware                   │  │
│  └────────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────┐   ┌──────────────────────────────┐   │
│  │  telepark/urls.py            │   │  settings.py                 │   │
│  │  ┌────────────────────────┐  │   │  - python-dotenv 1.2.2      │   │
│  │  │ path('admin/', ...)    │  │   │  - SECRET_KEY desde env     │   │
│  │  │ path('', include(...)) │  │   │  - ALLOWED_HOSTS desde env  │   │
│  │  └────────────────────────┘  │   │  - USE_TZ=True (zoneinfo)   │   │
│  └──────────────────────────────┘   │  - BigAutoField explícito   │   │
│                                     └──────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  teleparkApi  (aplicación DRF)                                          │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  urls.py (DRF Routers)                                          │   │
│  │  DefaultRouter(trailing_slash=False)                             │   │
│  │  ├── ViewSets registrados (16)                                  │   │
│  │  └── Endpoints directos (5) via path()                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐                   │
│  │  api.py              │    │  serializers.py      │                   │
│  │  ┌────────────────┐  │    │  ┌────────────────┐  │                   │
│  │  │ 16 ModelViewSets│  │    │  │ 25 Serializers │  │                   │
│  │  │ + 4 @action     │  │    │  │ (1 duplicado  │  │                   │
│  │  └────────────────┘  │    │  │  eliminado)    │  │                   │
│  └──────────────────────┘    │  └────────────────┘  │                   │
│                               └──────────────────────┘                   │
│                                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐                   │
│  │  authentication.py   │    │  handlers.py         │                   │
│  │  auth_view           │    │  CRUDHandlerStrategies│                  │
│  │  create_user         │    │  (dead code en       │                   │
│  │  update_user         │    │   views.py eliminado)│                   │
│  │  get_users           │    └──────────────────────┘                   │
│  └──────────────────────┘                                               │
│                                                                          │
│  ┌──────────────────────┐    ┌──────────────────────┐                   │
│  │  models.py           │    │  permission.py       │                   │
│  │  managed=False (26)  │    │  IsSuperuser         │                   │
│  │  SIN CAMBIOS         │    │                      │                   │
│  └──────────────────────┘    └──────────────────────┘                   │
└──────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────────┐
│  MySQL (sin cambios)                                                     │
│  Schema: teleparkbackend (pre-existente, managed=False)                  │
│  Conexión: mysqlclient 2.2.8                                            │
└──────────────────────────────────────────────────────────────────────────┘
```

### 7.2. Patrón Arquitectónico

| Aspecto | Detalle |
|---------|---------|
| **Patrón** | REST API con ViewSets + Routers (DRF) |
| **Estilo** | Resource-oriented (cada modelo = un ViewSet) |
| **Autenticación** | JWT Bearer Token via `rest_framework_simplejwt` |
| **Autorización** | `IsAuthenticated` global + `IsSuperuser` para endpoints de usuario |
| **Base de datos** | MySQL — modelos `managed=False` (espejo de BD existente) |
| **Configuración** | `python-dotenv` + variables de entorno (`.env`) |
| **Manejo de errores** | Middleware `ExceptionMiddleware` captura excepciones no manejadas y retorna `JsonResponse` |
| **Serialización** | DRF `ModelSerializer` con campos explícitos |
| **URL routing** | `DefaultRouter` para ViewSets CRUD + `path()` para endpoints de autenticación |

### 7.3. Stack de Dependencias Post-Estabilización

```
Django 5.2 LTS
├── asgiref 3.11.1
├── sqlparse 0.5.4
└── zoneinfo (stdlib, reemplaza pytz)
djangorestframework 3.17.1
djangorestframework-simplejwt 5.5.1
├── PyJWT 2.13.0
└── djangorestframework >=3.14
django-cors-headers 4.9.0
mysqlclient 2.2.8
python-dotenv 1.2.2
requests 2.34.2
├── urllib3 2.7.0
├── certifi 2026.05.20
├── charset-normalizer 3.3.x+
└── idna 3.7+
Jinja2 3.1.6
└── MarkupSafe 2.1.x+
simplejson 3.19.x
setuptools 82.0.1
```

---

## 8. Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Plan de Contingencia |
|----|--------|-------------|---------|------------|----------------------|
| R001 | **simplejwt 5.5.1 incompatible con Python 3.14** | **ALTA** (no está en matriz de pruebas oficial) | **CRÍTICO** — bloquea autenticación JWT | Verificación empírica aislada antes de Fase 5 (sección 5.1) | Implementar JWT con PyJWT 2.13.0 directo (sección 5.2) |
| R002 | **Django 5.2 requiere cambios en URL patterns** (`re_path` obsoleto) | **BAJA** — `re_path` sigue funcionando en 5.2 | **MEDIO** — warning de deprecación | Migración planificada a `path()` en Fases 6-7 | Si causa error, reportar y revertir (sección 2) |
| R003 | **mysqlclient 2.2.8 wheel no disponible para cp314** | **VERIFICADO DISPONIBLE** (REQUERIMIENTOS.md) | Ninguno si se verifica | Verificar en Fase 0 | Usar `PyMySQL==1.0.2` como alternativa (ya presente) |
| R004 | **urllib3 2.x rompe requests que usen API antigua** | **BAJA** — requests 2.34.2 encapsula urllib3 | **BAJO** — no se usa urllib3 directo | Actualizar requests junto con urllib3 (Fase 3) | Degradar a urllib3 1.26.x si hay errores de import |
| R005 | **SECRET_KEY ausente en entorno (post-migración)** | **MEDIA** — depende de despliegue | **ALTO** — Django no arranca | `os.getenv("SECRET_KEY")` sin default — forzar error temprano | Documentar en example.env como obligatorio; agregar chequeo en settings: `if not SECRET_KEY: raise ImproperlyConfigured(...)` |
| R006 | **B001 (basename duplicado) causa error en DRF 3.17** | **ALTA** — DRF 3.17 valida basenames únicos | **ALTO** — error de check impide arranque | Corrección programada en Fase 8 | Se corrige como parte del plan (REQ-13) |
| R007 | **USE_L10N eliminado causa error de configuración** | **ALTA** — eliminado en Django 5.0 | **ALTO** — Django 5.2 rechaza setting desconocido | Eliminar línea en Fase 5 (sección 3.5) | Si se omite, el error es claro y fácil de revertir |
| R008 | **pytz usado en runtime por algún import no detectado** | **BAJA** — no hay imports de pytz en el código | **MEDIO** — error de import en tiempo de ejecución | Verificación con grep antes de eliminar | Reinstalar pytz y reportar hallazgo |
| R009 | **CORS configurado con `['*']` causa inseguridad** | N/A — ya se corrige | N/A | Migrar ALLOWED_HOSTS desde env (sección 3.2) | Incluido en plan |
| R010 | **django-cors-headers 4.9.0 incompatible con Django 5.2** | **BAJA** — documentado compatible | **MEDIO** — error en check | Verificar en Fase 5 | Degradar a 4.8.x |

### Mapa de calor de riesgos

```
CRÍTICO:  R001
ALTO:     R005, R006, R007
MEDIO:    R002, R008, R010
BAJO:     R004, R009
VERIFICADO: R003 (disponible)
```

---

## 9. Contrato Vinculante

Las siguientes cláusulas son **innegociables** para este ciclo:

### 9.1. Cláusulas Técnicas

1. **Orden de fases respetado.** No se puede actualizar Django antes de completar Fase 1 (dead code) y Fase 3 (deps infra).
2. **SECRET_KEY migrada a variable de entorno** antes de la verificación `check --deploy`. No se acepta mantener la clave hardcodeada.
3. **USE_L10N eliminado de settings.py.** Django 5.2 no acepta este setting.
4. **pytz eliminado** de requirements.txt y del entorno. Reemplazado por `zoneinfo` (stdlib).
5. **BLACKLIST_AFTER_ROTATION = False** en simplejwt settings (no hay backend de blacklist).
6. **B001 corregido** (`basename='personaEp'` → `basename='personaP'` en PersonaPViewSet).
7. **re_path migrado a path()** en urls.py de ambas aplicaciones.
8. **CommonMiddleware duplicado eliminado** del MIDDLEWARE.
9. **No se modifican modelos, lógica de negocio, ni BD.**
10. **No se agregan tests nuevos.**

### 9.2. Cláusulas de Proceso

1. **Cada fase se commitea por separado** (commits atómicos). No se permite un solo commit gigante.
2. **Cada fase debe pasar `python manage.py check`** antes de avanzar a la siguiente.
3. **Al final de Fase 5** se ejecuta `python manage.py check --deploy` obligatoriamente.
4. **Si simplejwt 5.5.1 falla en Python 3.14** (R001), se activa el plan de contingencia (sección 5.2) sin bloquear el ciclo.
5. **No se corrigen B002 ni B003** a menos que la actualización los haga sintácticamente inválidos.
6. **El pipeline de CI debe ejecutar la suite de tests** (si existe) al final del ciclo. Si no existen tests, se documenta en CAMBIOS.md.

### 9.3. Exclusiones Explícitas (No cubiertas por este contrato)

- ✗ Migración a `drf-spectacular` (documentación de API)
- ✗ Corrección de B002 (asignación de clase `TipoEventoSerializer`)
- ✗ Corrección de B003 (ruta catch-all en `telepark/urls.py`)
- ✗ Instalación de blacklist backend para simplejwt
- ✗ Agregar tests unitarios o de integración
- ✗ Refactorización de `handlers.py` o `authentication.py`
- ✗ Cambios en `models.py` o migraciones de BD

---

## 10. Aprobación

| Rol | Estado | Fecha |
|-----|--------|-------|
| **Arquitecto** (emisor) | ✅ FIRMADO | 2026-07-02 |
| **Gatekeeper (DISEÑO)** | ⏳ PENDIENTE | — |
| **Orquestador** | ⏳ PENDIENTE | — |
| **Aprobación humana** | ⏳ PENDIENTE | — |

> **Pipeline bloqueado hasta:** `GATEKEEPER_CHECKPOINT` → `USER_CHECKPOINT`
> **Próximo paso:** Gatekeeper revisa contrato arquitectónico. Si aprueba, se pasa a estado `LISTO_PARA_DESARROLLO` y se invoca al Desarrollador.
