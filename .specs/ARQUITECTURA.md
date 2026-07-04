# ARQUITECTURA — Contrato Arquitectónico de Dockerización y Migración `managed`

> **Ciclo:** CICLO-20260702-002  
> **Fecha:** 2026-07-02  
> **Modo:** BROWNFIELD  
> **Artefacto:** Contrato vinculante para dockerización y cambio de `managed=False` → `managed=True`  
> **Precedencia:** Este documento tiene precedencia sobre decisiones técnicas ad-hoc. Solo puede ser modificado mediante aprobación explícita del orquestador.

---

## Índice

1. [Stack Tecnológico](#1-stack-tecnológico)
2. [Patrón Arquitectónico](#2-patrón-arquitectónico)
3. [Diseño de Componentes](#3-diseño-de-componentes)
4. [Plan de Migración de Datos](#4-plan-de-migración-de-datos)
5. [Variables de Entorno](#5-variables-de-entorno)
6. [Riesgos y Mitigaciones](#6-riesgos-y-mitigaciones)
7. [Contrato de Interfaces](#7-contrato-de-interfaces)
8. [Contrato Vinculante](#8-contrato-vinculante)

---

## 1. Stack Tecnológico

### 1.1. Stack Confirmado (post-CICLO-20260702-001)

| Componente | Versión | Estado |
|-----------|---------|--------|
| **Python** | 3.14.2 | ✅ Verificado en ciclo anterior |
| **Django** | 6.0.6 | ✅ Resuelto por pip en ciclo anterior |
| **djangorestframework** | 3.17.1 | ✅ Verificado |
| **djangorestframework-simplejwt** | 5.5.1 | ✅ Verificado |
| **mysqlclient** | 2.2.8 | ✅ Verificado (wheel disponible para cp314) |
| **PyMySQL** | 1.0.2 | 🟡 Fallback si mysqlclient falla en Docker |
| **django-cors-headers** | 4.9.0 | ✅ Verificado |
| **python-dotenv** | 1.2.2 | ✅ Verificado |
| **MySQL Server** | 8.0.x (imagen `mysql:8.0`) | 🆕 Se agrega para Docker |
| **Docker** | ≥ 24.0 | Requisito de entorno |
| **Docker Compose** | ≥ 2.20 | Requisito de entorno |

### 1.2. Dependencias Python (requirements.txt — 20 paquetes)

```
asgiref==3.11.1
certifi==2026.5.20
charset-normalizer==3.4.1
Django==6.0.6
django-cors-headers==4.9.0
djangorestframework==3.17.1
djangorestframework_simplejwt==5.5.1
idna==3.10
Jinja2==3.1.6
MarkupSafe==3.0.2
mysqlclient==2.2.8
PyJWT==2.13.0
PyMySQL==1.0.2          # Fallback driver
python-dotenv==1.2.2
requests==2.34.2
setuptools==82.0.1
simplejson==3.19.2
sqlparse==0.5.4
tzdata==2026.2
urllib3==2.7.0
```

### 1.3. Decisiones de Stack

| Decisión | Justificación |
|----------|---------------|
| **MySQL 8.0** en lugar de 8.4 o 9.x | `mysql:8.0` es la imagen más probada, estable, y compatible con `mysqlclient 2.2.8`. MySQL 8.4+ introduce cambios que podrían afectar la compatibilidad. |
| **`python:3.14-slim`** como base image | Python 3.14.2 es la versión del host. La variante `slim` reduce tamaño de imagen (~120 MB vs ~340 MB de `python:3.14`). |
| **PyMySQL 1.0.2 como fallback** | `mysqlclient` requiere compilar con librerías C nativas. Si la compilación falla en `python:3.14-slim` (por cambios en las cabeceras de MySQL 8.0), PyMySQL es un reemplazo directo sin dependencias nativas. |
| **Sin Gunicorn/uWSGI en desarrollo** | Para este ciclo, el servidor de desarrollo de Django (`manage.py runserver 0.0.0.0:8000`) es suficiente para QA. Gunicorn se agregará en un ciclo futuro si es necesario para producción. |

---

## 2. Patrón Arquitectónico

### 2.1. Estrategia de Migración `managed=False` → `managed=True`

#### 2.1.1. Análisis de Modelos Afectados

El archivo `teleparkApi/models.py` contiene **36 clases de modelos**, cada una con `managed = False` en su `class Meta`. Se clasifican en dos categorías:

| Categoría | Modelos | Cantidad | Estrategia |
|-----------|---------|----------|-----------|
| **A — Modelos de negocio** | Actividad, Actividadrealizada, Asistenciataller, Clasetaller, Comportamiento, Diagnostico, Direccion, Enfermedad, Evento, Evolucion, Factorclase, Factorglobal, Indicacionmedicamento, Localidad, Medicamento, Municipio, Obrasocial, Os, Persona, PersonaEp, Taller, Tipoevento, Tipoparentesco, Unidadobservacion, Valorvariableuo, Variableuo | **26** | Eliminar `managed = False` → Django asume `managed = True` (por defecto) |
| **B — Modelos del framework Django** | AuthGroup, AuthGroupPermissions, AuthPermission, AuthUser, AuthUserGroups, AuthUserUserPermissions, DjangoAdminLog, DjangoContentType, DjangoMigrations, DjangoSession | **10** | **Conflictivos** — ver sección 2.1.3 |

#### 2.1.2. Estrategia para Modelos de Negocio (Categoría A)

**Acción:** Eliminar la línea `managed = False` de la clase `Meta` en los 26 modelos de negocio.

```python
# ANTES
class Persona(models.Model):
    ...
    class Meta:
        managed = False
        db_table = 'persona'

# DESPUÉS
class Persona(models.Model):
    ...
    class Meta:
        db_table = 'persona'
        # managed = True  (implícito, no se agrega)
```

**Justificación:** Django usa `managed = True` como valor por defecto. No se agrega explícitamente para no ensuciar el código. La ausencia de `managed = False` es equivalente a `managed = True`.

**Efecto en migraciones:** Al ejecutar `makemigrations`, Django detectará que estos modelos ahora son "managed" y generará operaciones `CreateModel` en una nueva migración. Al ejecutar `migrate`, Django creará las tablas en la base de datos.

#### 2.1.3. Estrategia para Modelos del Framework Django (Categoría B)

**Problema:** Los modelos AuthGroup, AuthUser, DjangoContentType, etc. son tablas internas de Django que ya son creadas y administradas por las aplicaciones `django.contrib.auth`, `django.contrib.contenttypes`, etc. Si se cambian a `managed = True` en `teleparkApi`, habrá **conflicto de migraciones**: dos aplicaciones distintas (`django.contrib.auth` y `teleparkApi`) intentarán administrar las mismas tablas.

**Alternativas evaluadas:**

| Alternativa | Descripción | Pros | Contras |
|-------------|-------------|------|---------|
| **A-1 (Recomendada)** | Eliminar los 10 modelos Django de `teleparkApi/models.py` | ✅ Elimina el conflicto raíz. Django ya los gestiona. Limpia 166 líneas de código muerto. | ⚠️ Fuera de alcance según REQUERIMIENTOS.md ("No se tocan los modelos") |
| **A-2** | Mantener `managed = False` solo en los 10 modelos Django | ✅ Mínimo cambio. Sin conflicto. | ❌ Incumple REQ-01 ("Todos los modelos DEBEN tener managed=True") |
| **A-3** | Mantener `managed = False` en los 10 modelos Django + documentar como excepción técnica justificada | ✅ Práctico. Sin riesgo de migración. | ❌ Incumple REQ-01 textualmente |
| **A-4** | Cambiar a `managed = True` y forzar orden de migraciones con `migration_depends_on` | ✅ Cumple REQ-01 al pie de la letra | ❌ Alto riesgo: conflictos difíciles de debuggear en `migrate`. Las tablas se crearían dos veces. |

**Decisión arquitectónica:** Se recomienda **Alternativa A-1** (eliminar modelos Django de models.py) como la solución más limpia y correcta desde el punto de vista arquitectónico. Sin embargo, dado que el alcance del ciclo dice explícitamente "Solo cambios de managed + dockerización", se adopta la **Alternativa A-3 como plan primario** y **A-1 como contingencia** si surgen conflictos.

**Plan primario (A-3):**
- En los 26 modelos de negocio: eliminar `managed = False`
- En los 10 modelos Django: mantener `managed = False` (no se modifica su clase Meta)
- Se documenta en `CAMBIOS.md` que estos 10 modelos se excluyen por ser tablas gestionadas por Django internamente

**Plan de contingencia (A-1):** Si al ejecutar `makemigrations` Django genera migraciones conflictivas para las tablas del framework, se procederá a eliminar los 10 modelos Django de `models.py`.

### 2.2. Estrategia de Dockerización

#### 2.2.1. Topología

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DOCKER COMPOSE ENVIRONMENT                           │
│                                                                             │
│  ┌──────────────────────────┐     ┌──────────────────────────┐             │
│  │  Servicio: db            │     │  Servicio: app           │             │
│  │  Imagen: mysql:8.0       │     │  Imagen: python:3.14-slim│             │
│  │  Puerto: 3306 (interno)  │◀────│  Puerto: 8000 (host)     │             │
│  │  Volumen: mysql_data     │     │  depends_on: db (health) │             │
│  │  Healthcheck: ✓          │     │  Entrypoint: wait+ migrate │           │
│  └──────────────────────────┘     └──────────────────────────┘             │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Red: telepark-network (bridge)                                      │   │
│  │  Servicios se descubren como: db:3306, app:8000                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### 2.2.2. Flujo de Inicio

```
docker-compose up
    │
    ├──▶ Servicio db: mysql:8.0
    │       │
    │       ├──▶ Crea volumen mysql_data (si no existe)
    │       ├──▶ Inicializa BD con variables de entorno
    │       ├──▶ Healthcheck: mysqladmin ping (cada 10s)
    │       └──▶ Estado: healthy
    │
    └──▶ Servicio app: python:3.14-slim
            │
            ├──▶ Build: Dockerfile
            ├──▶ Entrypoint: entrypoint.sh
            │       │
            │       ├──▶ Wait-for-it: loop hasta que db:3306 responda
            │       │      (timeout: 60s, retry cada 3s)
            │       │
            │       ├──▶ python manage.py makemigrations teleparkApi
            │       │      (genera migraciones para modelos con managed=True)
            │       │
            │       ├──▶ python manage.py migrate
            │       │      (aplica migraciones → crea tablas en MySQL)
            │       │
            │       └──▶ python manage.py runserver 0.0.0.0:8000
            │
            └──▶ Servidor Django escuchando en :8000
```

#### 2.2.3. Gestión de Migraciones Existentes

Actualmente existen migraciones en `teleparkApi/migrations/`:
- `0001_initial.py` (187 líneas)
- `0002_authgroup_authgrouppermissions_...py` (133 líneas)

Estas migraciones fueron generadas con `managed = False` y su estado de aplicación es incierto (el proyecto nunca tuvo una base de datos local). Para el entorno dockerizado:

**Estrategia:** Eliminar las migraciones existentes y regenerarlas desde cero. Esto asegura que:
1. Las nuevas migraciones reflejen el estado actual de los modelos (sin `managed = False`)
2. No haya conflictos de migraciones previas con la base de datos limpia
3. La migración inicial contenga operaciones `CreateModel` que Django ejecutará al hacer `migrate`

**Acción en entrypoint.sh:**
```bash
# Las migraciones viejas se eliminan en el Dockerfile
# entrypoint solo ejecuta makemigrations y migrate
python manage.py makemigrations teleparkApi
python manage.py migrate
```

> **Nota:** Si en el futuro se conecta a una base de datos existente (no dockerizada), las tablas ya existen en MySQL. Django detectará el estado y no intentará recrearlas si detecta que la estructura coincide (operación idempotente). Si hay diferencias, Django creará migraciones de alteración.

---

## 3. Diseño de Componentes

### 3.1. Capa de Modelos (models.py)

#### 3.1.1. Plan de Modificación

| Archivo | Acción | Detalle |
|---------|--------|---------|
| `teleparkApi/models.py` | **ELIMINAR** `managed = False` | En las 26 clases `Meta` de modelos de negocio |
| `teleparkApi/models.py` | **MANTENER** `managed = False` | En las 10 clases `Meta` de modelos del framework Django |

**Cambio exacto por modelo (26 ocurrencias):**

```python
# Patrón de cambio para cada modelo de negocio:
# De:
    class Meta:
        managed = False
        db_table = 'nombre_tabla'

# A:
    class Meta:
        db_table = 'nombre_tabla'
```

**Modelos afectados (26):**

| # | Modelo | db_table |
|---|--------|----------|
| 1 | Actividad | actividad |
| 2 | Actividadrealizada | actividadrealizada |
| 3 | Asistenciataller | asistenciataller |
| 4 | Clasetaller | clasetaller |
| 5 | Comportamiento | comportamiento |
| 6 | Diagnostico | diagnostico |
| 7 | Direccion | direccion |
| 8 | Enfermedad | enfermedad |
| 9 | Evento | evento |
| 10 | Evolucion | evolucion |
| 11 | Factorclase | factorclase |
| 12 | Factorglobal | factorglobal |
| 13 | Indicacionmedicamento | indicacionmedicamento |
| 14 | Localidad | localidad |
| 15 | Medicamento | medicamento |
| 16 | Municipio | municipio |
| 17 | Obrasocial | obrasocial |
| 18 | Os | os |
| 19 | Persona | persona |
| 20 | PersonaEp | personaep |
| 21 | Taller | taller |
| 22 | Tipoevento | tipoevento |
| 23 | Tipoparentesco | tipoparentesco |
| 24 | Unidadobservacion | unidadobservacion |
| 25 | Valorvariableuo | valorvariableuo |
| 26 | Variableuo | variableuo |

**Modelos NO modificados (10) — mantienen `managed = False`:**

| # | Modelo | Razón |
|---|--------|-------|
| 1 | AuthGroup | Gestionado por `django.contrib.auth` |
| 2 | AuthGroupPermissions | Gestionado por `django.contrib.auth` |
| 3 | AuthPermission | Gestionado por `django.contrib.auth` |
| 4 | AuthUser | Gestionado por `django.contrib.auth` |
| 5 | AuthUserGroups | Gestionado por `django.contrib.auth` |
| 6 | AuthUserUserPermissions | Gestionado por `django.contrib.auth` |
| 7 | DjangoAdminLog | Gestionado por `django.contrib.admin` |
| 8 | DjangoContentType | Gestionado por `django.contrib.contenttypes` |
| 9 | DjangoMigrations | Gestionado por Django internamente |
| 10 | DjangoSession | Gestionado por `django.contrib.sessions` |

#### 3.1.2. Estrategia para Migraciones Iniciales (CreateModel)

Las migraciones existentes (`0001_initial.py`, `0002_authgroup_...py`) serán **eliminadas** como parte de la dockerización. El entrypoint ejecutará:

```bash
# Paso 1: Eliminar migraciones antiguas del contenedor
# (se hace en Dockerfile: RUN rm -f teleparkApi/migrations/0*.py)

# Paso 2: Generar nuevas migraciones
python manage.py makemigrations teleparkApi
# → Crea: teleparkApi/migrations/0001_initial.py con CreateModel para los 26 modelos

# Paso 3: Aplicar migraciones (crea tablas en MySQL)
python manage.py migrate
# → Crea: auth_user, auth_group, ..., luego actividad, persona, etc.
```

**Comportamiento esperado de `makemigrations`:**
- Django analiza `teleparkApi/models.py`
- Detecta modelos con `db_table` definido y `managed = True` (por defecto)
- Genera operaciones `migrations.CreateModel` con `options={'db_table': 'nombre'}`
- La migración generada NO incluye `managed = False` en las opciones de CreateModel

**Comportamiento esperado de `migrate`:**
- Django aplica primero sus migraciones internas (auth, contenttypes, admin, sessions)
- Django aplica migraciones de terceros (si las hubiera)
- Django aplica `0001_initial` de `teleparkApi`
- Para cada `CreateModel`, Django ejecuta `CREATE TABLE ...` con el schema definido en el modelo

#### 3.1.3. Verificación Post-Migración

```sql
-- Conectarse al contenedor MySQL:
docker exec -it telepark-db-1 mysql -uteleparkUser -pteleparkUser teleparkbackend

-- Verificar tablas creadas:
SHOW TABLES;

-- Deberían aparecer:
-- | actividad              |
-- | actividadrealizada     |
-- | asistenciataller       |
-- | ... (26 tablas de negocio)
-- | auth_group             |
-- | auth_user              |
-- | ... (tablas del framework)
```

### 3.2. Dockerización

#### 3.2.1. Dockerfile

**Ubicación:** `D:\TELEPARK\backend\telepark-backend\Dockerfile`

**Especificación:**

```dockerfile
# ============================================================
# Dockerfile — Telepark Backend
# Base: python:3.14-slim
# Django 6.0.6 + DRF 3.17.1 + MySQL 8.0
# ============================================================

FROM python:3.14-slim AS builder

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instalar dependencias de compilación para mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (caching de capas)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

# ============================================================
# Imagen final (más liviana)
# ============================================================
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Solo runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar Python instalado desde builder
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar proyecto
COPY . .

# Eliminar migraciones antiguas (se regenerarán en entrypoint)
RUN rm -f teleparkApi/migrations/0*.py

# Crear directorio static si no existe (evita warning de Django)
RUN mkdir -p static

# Puerto de exposición
EXPOSE 8000

# Entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

**Versión simplificada (sin multi-stage, más simple de mantener):**

```dockerfile
# Alternativa: Dockerfile de una sola etapa
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instalar dependencias de compilación y runtime para mysqlclient
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

COPY . .

# Eliminar migraciones antiguas para regenerar desde cero
RUN rm -f teleparkApi/migrations/0*.py
RUN mkdir -p static

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
```

> **Decisión:** Se prefiere el Dockerfile de una sola etapa para este ciclo por simplicidad. La versión multi-stage se puede adoptar en un ciclo futuro si el tamaño de la imagen es una preocupación.

#### 3.2.2. docker-compose.yml

**Ubicación:** `D:\TELEPARK\backend\telepark-backend\docker-compose.yml`

**Especificación:**

```yaml
version: "3.8"

services:
  db:
    image: mysql:8.0
    container_name: telepark-db
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${DB_DATABASE:-teleparkbackend}
      MYSQL_USER: ${DB_USER:-teleparkUser}
      MYSQL_PASSWORD: ${DB_PASSWORD:-teleparkUser}
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:-rootpassword}
    ports:
      - "3307:3306"   # Puerto host diferente para no conflictuar con MySQL local
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p$$MYSQL_ROOT_PASSWORD"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - telepark-network

  app:
    build: .
    container_name: telepark-app
    restart: unless-stopped
    depends_on:
      db:
        condition: service_healthy
    environment:
      DB_HOST: db
      DB_PORT: "3306"
      DB_DATABASE: ${DB_DATABASE:-teleparkbackend}
      DB_USER: ${DB_USER:-teleparkUser}
      DB_PASSWORD: ${DB_PASSWORD:-teleparkUser}
      SECRET_KEY: ${SECRET_KEY:-django-insecure-dev-key-not-for-production}
      ALLOWED_HOSTS: ${ALLOWED_HOSTS:-localhost,127.0.0.1}
      CSRF_TRUSTED_ORIGINS: ${CSRF_TRUSTED_ORIGINS:-http://localhost:8000}
      SITE_URL: ${SITE_URL:-http://localhost:8000}
      ENV: ${ENV:-dev}
    ports:
      - "8000:8000"
    volumes:
      - .:/app          # Monta el código para desarrollo hot-reload
    networks:
      - telepark-network

volumes:
  mysql_data:
    name: telepark_mysql_data

networks:
  telepark-network:
    name: telepark-network
    driver: bridge
```

**Detalles de diseño:**

| Elemento | Decisión | Justificación |
|----------|----------|---------------|
| `container_name` explícito | Sí | Facilita identificación en `docker ps` |
| Puerto MySQL host: `3307` | 3307 (no 3306) | Evita conflictos con MySQL local del desarrollador |
| `depends_on` con `condition: service_healthy` | Sí | Asegura que MySQL esté listo antes de iniciar Django |
| Volumen `mysql_data` con nombre | `telepark_mysql_data` | Persistencia de datos entre reinicios |
| Red `telepark-network` driver bridge | Sí | Aislamiento de red. Servicios se descubren por nombre de servicio |
| `volumes: .:/app` en app | Sí | Hot-reload durante desarrollo |

#### 3.2.3. entrypoint.sh

**Ubicación:** `D:\TELEPARK\backend\telepark-backend\entrypoint.sh`

**Especificación:**

```bash
#!/bin/bash
# entrypoint.sh — Telepark Backend
# Espera a MySQL, ejecuta migraciones, inicia Django

set -e

# Variables de conexión
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-3306}"
DB_USER="${DB_USER:-teleparkUser}"
DB_PASSWORD="${DB_PASSWORD:-teleparkUser}"
DB_DATABASE="${DB_DATABASE:-teleparkbackend}"
TIMEOUT=60
INTERVAL=3

echo "⏳ Esperando a MySQL en $DB_HOST:$DB_PORT ..."

# Loop de espera con timeout
elapsed=0
while ! mysqladmin ping -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" --silent 2>/dev/null; do
    elapsed=$((elapsed + INTERVAL))
    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        echo "❌ ERROR: MySQL no está disponible después de ${TIMEOUT}s"
        echo "   Host: $DB_HOST:$DB_PORT"
        echo "   User: $DB_USER"
        exit 1
    fi
    echo "   MySQL no responde aún... (${elapsed}s/${TIMEOUT}s)"
    sleep $INTERVAL
done

echo "✅ MySQL está listo."

# Verificar conectividad con Django
echo "🔍 Verificando configuración de Django..."
python manage.py check --deploy 2>&1 | grep -v "WARNINGS" || true

# Generar migraciones
echo "📦 Ejecutando makemigrations teleparkApi..."
python manage.py makemigrations teleparkApi

# Aplicar migraciones
echo "🗄️ Ejecutando migrate..."
python manage.py migrate

# Verificar resultado
echo "✅ Migraciones aplicadas correctamente."

# Iniciar servidor de desarrollo
echo "🚀 Iniciando servidor Django en 0.0.0.0:8000..."
exec python manage.py runserver 0.0.0.0:8000
```

**Requisitos del entrypoint:**
- `mysql-client` debe estar instalado en el contenedor (incluido en `default-libmysqlclient-dev` o instalado explícitamente)
- Alternativa: usar `python -c "import MySQLdb; MySQLdb.connect(...)"` si mysqladmin no está disponible

**Estrategia alternativa (sin mysqladmin):**

```bash
# Alternativa: usar Python para probar conexión
python -c "
import MySQLdb
import time
import sys

host = '${DB_HOST}'
port = int('${DB_PORT}')
user = '${DB_USER}'
password = '${DB_PASSWORD}'
database = '${DB_DATABASE}'

timeout = 60
elapsed = 0
while elapsed < timeout:
    try:
        conn = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=database)
        conn.close()
        print('MySQL connection OK')
        sys.exit(0)
    except Exception as e:
        elapsed += 3
        print(f'Waiting for MySQL... ({elapsed}s/{timeout}s)')
        time.sleep(3)
print('ERROR: MySQL connection timeout')
sys.exit(1)
"
```

#### 3.2.4. .dockerignore

**Ubicación:** `D:\TELEPARK\backend\telepark-backend\.dockerignore`

**Especificación:**

```
.git
.gitignore
.venv
.vscode
__pycache__
*.pyc
.env
example.env
BD/
README.md
package-lock.json
```

### 3.3. Endpoint de Healthcheck (Opcional — REQ-13)

Se especifica un endpoint opcional `/api/health/` implementado como vista simple de Django:

**Especificación del contrato:**

| Atributo | Valor |
|----------|-------|
| **Ruta** | `GET /api/health/` |
| **Propósito** | Verificar que la aplicación y la BD responden |
| **Autenticación** | No requiere (público) |
| **Respuesta exitosa** | `{"status": "ok", "database": "connected", "tables": 26}` |
| **Respuesta fallo BD** | `{"status": "error", "database": "disconnected", "detail": "..."}` (HTTP 503) |
| **Códigos HTTP** | 200 OK / 503 Service Unavailable |

**Verificaciones que debe realizar:**
1. Conexión a base de datos (ejecutar `Persona.objects.first()` o similar)
2. Contar tablas de negocio disponibles

**Cobertura de REQ-13:** REQ-13 es un criterio `Optional-feature`. Se implementa si el equipo lo considera necesario para QA, pero no bloquea el ciclo.

---

## 4. Plan de Migración de Datos

### 4.1. Escenario Dockerizado (entorno limpio)

| Paso | Acción | Resultado |
|------|--------|-----------|
| 1 | `docker-compose up -d db` | Contenedor MySQL inicia, crea BD y usuario |
| 2 | `docker-compose up -d app` | Contenedor Django construye y arranca |
| 3 | Entrypoint: `makemigrations teleparkApi` | Genera `0001_initial.py` con CreateModel para 26 modelos |
| 4 | Entrypoint: `migrate` | Crea 26 tablas de negocio + tablas del framework Django |
| 5 | QA verifica con `docker exec` | `SHOW TABLES` → 26 tablas de negocio presentes |

**No hay migración de datos porque no hay datos previos.** Es un entorno fresco.

### 4.2. Escenario con BD Existente (producción/staging)

Si en el futuro este diseño se aplica a una base de datos existente (con datos reales), el comportamiento esperado es:

| Condición | Comportamiento de `migrate` | Riesgo |
|-----------|---------------------------|--------|
| Tablas existen con misma estructura que modelos | `migrate` detecta que las tablas ya existen y las marca como sincronizadas (registra en `django_migrations`) | 🟢 Ninguno |
| Tablas existen pero estructura diferente | `migrate` ejecutará `ALTER TABLE` si hay diferencias. Puede fallar si hay datos incompatibles | 🟡 Medio — requiere revisión manual |
| Tablas no existen | `migrate` ejecuta `CREATE TABLE` | 🟢 Sin riesgo |

**Recomendación para escenario brownfield con datos reales:**
1. Hacer backup completo de la BD antes de aplicar migraciones
2. Ejecutar `python manage.py migrate --fake-initial` si las tablas ya existen y coinciden exactamente
3. Verificar con `python manage.py showmigrations` que todas las migraciones estén marcadas como `[X]`

### 4.3. Estrategia de Rollback para models.py

Si el cambio de `managed = True` causa problemas:

```bash
# Revertir cambios en models.py (restaurar managed=False)
git checkout -- teleparkApi/models.py

# En Docker: reconstruir imagen
docker-compose down -v
docker-compose build --no-cache app
docker-compose up -d
```

---

## 5. Variables de Entorno

### 5.1. Lista Completa

| Variable | Obligatoria | Valor por Defecto | Descripción | Usada en |
|----------|-------------|-------------------|-------------|----------|
| `DB_DATABASE` | Sí | `teleparkbackend` | Nombre de la base de datos MySQL | settings.py, docker-compose.yml, entrypoint.sh |
| `DB_HOST` | Sí | `localhost` (local) / `db` (Docker) | Host del servidor MySQL | settings.py, docker-compose.yml, entrypoint.sh |
| `DB_PORT` | Sí | `3306` | Puerto del servidor MySQL | settings.py, docker-compose.yml, entrypoint.sh |
| `DB_USER` | Sí | `teleparkUser` | Usuario de MySQL | settings.py, docker-compose.yml, entrypoint.sh |
| `DB_PASSWORD` | Sí | — | Contraseña de MySQL | settings.py, docker-compose.yml, entrypoint.sh |
| `DB_ROOT_PASSWORD` | Sí (Docker) | `rootpassword` | Contraseña root de MySQL (solo para Docker) | docker-compose.yml |
| `SECRET_KEY` | Sí | — | Clave secreta de Django | settings.py |
| `ALLOWED_HOSTS` | No | `localhost` | Hosts permitidos separados por coma | settings.py |
| `CSRF_TRUSTED_ORIGINS` | No | `http://localhost:8000` | Orígenes confiables para CSRF | settings.py |
| `SITE_URL` | No | `http://localhost:8000` | URL del sitio para CORS | settings.py |
| `ENV` | No | `dev` | Entorno (`dev`/`prod`). `dev` activa DEBUG | settings.py |

### 5.2. Mapeo settings.py ↔ Variables de Entorno

```python
# telepark/settings.py
SECRET_KEY = os.getenv("SECRET_KEY")                    # REQUERIDO
DEBUG = os.getenv("ENV") == 'dev'                       # dev → True
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
CSRF_TRUSTED_ORIGINS = [os.getenv("CSRF_TRUSTED_ORIGINS")]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_DATABASE"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
    }
}
```

### 5.3. example.env (actualizado para Docker)

```
# ============================================================
# Telepark — Variables de Entorno
# ============================================================

# MySQL Connection
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=teleparkbackend
DB_USER=teleparkUser
DB_PASSWORD=teleparkUser
DB_ROOT_PASSWORD=rootpassword

# Django Security
SECRET_KEY=django-insecure-5@j$75afof+#p%ft9d4e!)x7%_8na_3arrrb19k1enrjz*g+%u
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
SITE_URL=http://localhost:8000

# Environment
ENV=dev
```

### 5.4. Configuración para Docker

Cuando se ejecuta con Docker Compose, las variables se pasan desde el archivo `.env` o desde el entorno del host. Docker Compose carga automáticamente un archivo `.env` si existe en el mismo directorio.

```yaml
# docker-compose.yml extrae automáticamente:
# - Variables de entorno del host
# - Variables del archivo .env (si existe)
# - Valores por defecto definidos en docker-compose.yml
```

---

## 6. Riesgos y Mitigaciones

### 6.1. Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación | Plan de Contingencia |
|----|--------|-------------|---------|------------|----------------------|
| R001 | **mysqlclient no compila en python:3.14-slim** | Media | Alto — bloquea migraciones | Instalar dependencias de compilación (gcc, default-libmysqlclient-dev) en Dockerfile | Usar `PyMySQL==1.0.2` como engine alternativo (ya en requirements.txt). Cambiar `ENGINE` a `'django.db.backends.mysql'` con PyMySQL instalado como driver |
| R002 | **Conflicto de migraciones entre modelos Django (auth/admin) y teleparkApi** | Alta | Alto — `migrate` falla | Mantener `managed=False` en los 10 modelos Django (Categoría B) | Eliminar modelos Django de models.py (Alternativa A-1) |
| R003 | **makemigrations no genera CreateModel para modelos con db_table** | Baja | Alto — tablas no se crean | Verificar que `managed=False` se eliminó correctamente. Django trata modelos sin `managed=False` como managed por defecto | Forzar `managed = True` explícito en la clase Meta como fallback |
| R004 | **MySQL container no ready timeout en entrypoint** | Baja | Medio — app no arranca | Healthcheck configurado con `start_period: 30s` y retry 5 | Aumentar `TIMEOUT` en entrypoint.sh de 60s a 120s |
| R005 | **Puerto 3306 conflictua con MySQL local del host** | Alta (dev) | Bajo — error de bind | Usar puerto host `3307` en docker-compose.yml | Cambiar a `3308` o puerto no utilizado |
| R006 | **`makemigrations` falla porque las migraciones antiguas tienen conflictos** | Media | Medio — bloquea generación | Eliminar migraciones antiguas (`0*.py`) en Dockerfile | Mantener migraciones antiguas y usar `--name` para crear migraciones con nombre diferente |
| R007 | **Django 6.0.6 incompatible con mysqlclient 2.2.8** | Baja | Alto — no conexión a BD | mysqlclient 2.2.8 es estable y compatible con Django 4.x-6.x | Usar `PyMySQL==1.0.2` como engine alternativo |
| R008 | **Los modelos con `db_column` con mayúsculas causan problemas con MySQL en Linux** | Baja | Medio — diferencias case-sensitive | MySQL en Linux es case-sensitive para nombres de tabla. `db_table` usa minúsculas | Verificar que `db_table` siempre está en minúsculas en los modelos |
| R009 | **Volumen mysql_data persiste datos corruptos entre recreaciones** | Baja | Medio — datos inconsistentes | Usar `docker-compose down -v` para eliminar volúmenes al hacer limpieza | Documentar procedimiento de limpieza |
| R010 | **Healthcheck con mysqladmin no disponible en contenedor slim** | Media | Medio — no se puede verificar salud | No depende de mysqladmin; usar script Python de conexión como alternativa en entrypoint.sh | Instalar mysql-client en Dockerfile |

### 6.2. Mapa de Calor

```
ALTO:     R002 (Conflicto migraciones)
ALTO:     R001 (mysqlclient no compila)
MEDIO:    R006 (Migraciones antiguas)
MEDIO:    R004 (Timeout MySQL)
MEDIO:    R010 (mysqladmin no disponible)
BAJO:     R003 (CreateModel no generado)
BAJO:     R005 (Puerto conflictivo)
BAJO:     R007 (Incompatibilidad Django-mysqlclient)
BAJO:     R008 (Case sensitivity)
BAJO:     R009 (Volumen corrupto)
```

### 6.3. OWASP Compliance

| Requisito OWASP | Implementación en este ciclo |
|----------------|----------------------------|
| **A01 — Broken Access Control** | Se mantiene `IsAuthenticated` global en ViewSets (heredado). El healthcheck `/api/health/` es público por diseño |
| **A02 — Cryptographic Failures** | `SECRET_KEY` ya migrada a variable de entorno en ciclo anterior. Conexión MySQL dentro de Docker sin TLS (red interna bridge). Para producción se debe habilitar TLS |
| **A03 — Injection** | Django ORM protege contra inyección SQL. No se usan raw queries. Validación con DRF Serializers |
| **A04 — Insecure Design** | El diseño sigue el patrón de capas definido en GLOBAL_RULES.md |
| **A05 — Security Misconfiguration** | Variables de entorno validadas. Puerto 3307 en host evita conflictos |
| **A06 — Vulnerable Components** | Todas las dependencias actualizadas a versiones seguras en ciclo anterior |
| **A07 — Authentication Failures** | JWT con simplejwt 5.5.1. Tokens con expiración (60 min access, 1 día refresh) |
| **A08 — Software Integrity** | Dockerfile construye desde fuente. requirements.txt con versiones fijas |
| **A09 — Logging & Monitoring** | No implementado en este ciclo. Pendiente para ciclo futuro |
| **A10 — SSRF** | No aplica (no hay fetch a URLs externas) |

---

## 7. Contrato de Interfaces

### 7.1. Puertos

| Servicio | Puerto Contenedor | Puerto Host | Protocolo | Propósito |
|----------|------------------|-------------|-----------|-----------|
| **app** (Django) | 8000 | 8000 | TCP/HTTP | API REST |
| **db** (MySQL) | 3306 | 3307 (nota 1) | TCP/MySQL | Base de datos |

> **Nota 1:** Se usa puerto host `3307` para no conflictuar con instalaciones MySQL locales que usualmente ocupan el 3306. Internamente, los contenedores se comunican por el puerto 3306.

### 7.2. Red

| Nombre | Driver | Propósito |
|--------|--------|-----------|
| `telepark-network` | bridge | Red aislada para comunicación entre contenedores |

**Nombres de host dentro de la red:**
- `db` → resuelve al contenedor MySQL (puerto 3306)
- `app` → resuelve al contenedor Django (puerto 8000)

### 7.3. Endpoints de API (Afectados por este ciclo)

| Método | Ruta | Cambio | Autenticación |
|--------|------|--------|---------------|
| GET | `/api/health/` | 🆕 Nuevo (opcional — REQ-13) | Pública |

El resto de los endpoints (~80+) heredados de ciclos anteriores no se modifican.

### 7.4. Volúmenes

| Nombre | Mount point | Propósito |
|--------|-------------|-----------|
| `telepark_mysql_data` | `/var/lib/mysql` | Persistencia de datos MySQL entre reinicios |

### 7.5. Nombres de Contenedor

| Servicio | container_name | Hostname (red interna) |
|----------|---------------|----------------------|
| db | `telepark-db` | `db` |
| app | `telepark-app` | `app` |

---

## 8. Contrato Vinculante

### 8.1. Cláusulas Técnicas

1. **`managed = False` se elimina exclusivamente de los 26 modelos de negocio.** Los 10 modelos del framework Django (Auth*, Django*) mantienen `managed = False` para evitar conflictos de migraciones.
2. **Las migraciones existentes se eliminan** (`teleparkApi/migrations/0*.py`) y se regeneran en el entrypoint.
3. **El entrypoint.sh** es responsable de la secuencia: wait-for-mysql → makemigrations → migrate → runserver.
4. **MySQL se expone en puerto host 3307**, no 3306, para evitar conflictos.
5. **La imagen base es `python:3.14-slim`** con las dependencias de compilación necesarias para mysqlclient.
6. **PyMySQL 1.0.2** se mantiene en requirements.txt como fallback si mysqlclient falla.
7. **No se modifican modelos, lógica de negocio, ni estructura de tablas.** Solo se cambia el atributo `managed` en la clase `Meta`.
8. **No se agregan datos seed ni fixtures.** La BD se crea vacía.

### 8.2. Cláusulas de Proceso

1. **El ciclo se ejecuta en orden:** models.py → Dockerfile → docker-compose.yml → entrypoint.sh → .dockerignore → verificación.
2. **Cada cambio en models.py debe pasar `python manage.py check`** antes de construir la imagen Docker.
3. **La verificación final** consiste en `docker-compose up` exitoso + verificación de tablas via `docker exec`.
4. **Si mysqlclient falla en la compilación Docker**, se activa el plan de contingencia (PyMySQL) sin bloquear el ciclo.
5. **Si `makemigrations` genera migraciones conflictivas** (ej. para modelos Django), se eliminan los modelos conflictivos de models.py.

### 8.3. Cobertura de Requerimientos

| User Story | Criterios EARS | Cobertura Arquitectónica |
|------------|---------------|--------------------------|
| **US-01** | REQ-01, REQ-10, REQ-12 | Sección 2.1 (estrategia managed) + Sección 3.1 (plan de modificación) |
| **US-02** | REQ-02, REQ-03, REQ-04, REQ-07, REQ-08, REQ-11 | Sección 3.2 (Dockerfile, docker-compose, entrypoint) |
| **US-03** | REQ-05, REQ-06 | Sección 3.1.2 (estrategia migraciones) + entrypoint.sh |
| **US-04** | REQ-09, REQ-13 | Sección 3.3 (healthcheck) + Sección 7.3 (endpoints) |

### 8.4. Exclusiones Explícitas

- ✗ Modificación de campos, tipos de dato, o relaciones en modelos
- ✗ Eliminación de modelos Django de models.py (a menos que sea necesario por conflicto)
- ✗ Implementación de autenticación adicional
- ✗ Tests unitarios o de integración
- ✗ Configuración de Gunicorn/uWSGI para producción
- ✗ Configuración de TLS/SSL
- ✗ Implementación de logging estructurado
- ✗ Seed de datos o fixtures

---

## Aprobación

| Rol | Estado | Fecha |
|-----|--------|-------|
| **Arquitecto** (emisor) | ✅ FIRMADO | 2026-07-02 |
| **Gatekeeper (DISEÑO)** | ⏳ PENDIENTE | — |
| **Orquestador** | ⏳ PENDIENTE | — |
| **Aprobación humana** | ⏳ PENDIENTE | — |

> **Pipeline bloqueado hasta:** Revisión del Gatekeeper y aprobación humana.
> **Próximo paso:** Gatekeeper revisa el contrato arquitectónico. Si aprueba, se notifica al Orquestador para proceder a `LISTO_PARA_DESARROLLO`.
