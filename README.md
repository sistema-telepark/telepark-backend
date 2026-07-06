# Telepark Backend

API REST para la gestión integral de personas, salud, eventos, obra social y talleres en una institución.

## Stack

| Componente | Versión |
|---|---|
| Python | 3.14.2 |
| Django | 6.0.6 |
| Django REST Framework | 3.17.1 |
| MySQL | 8.0 |
| djangorestframework-simplejwt | 5.4.0 |
| drf-spectacular | 0.29.0 |

## Arquitectura

Monolito modular (**modulith**) con 7 apps organizadas en dos capas:

**Infraestructura interna**
- `usuarios` — autenticación JWT, registro y gestión de usuarios (wrapper sobre `django.contrib.auth.User`)
- `core` — router central, middleware de errores, permisos, health check

**Dominio de negocio**
- `personas` — módulo raíz: personas, direcciones, localidades, parentescos
- `salud` — diagnósticos, evoluciones, enfermedades, medicamentos
- `eventos` — eventos y tipos de evento
- `obra_social` — obras sociales y coberturas
- `talleres` — talleres, clases, actividades, asistencia, observaciones

Las dependencias entre módulos forman un **DAG acíclico** donde todas las FKs cruzadas apuntan exclusivamente a `personas`.

Cada módulo sigue una **capa de 3 niveles**: Views/Serializers → Services → Models. La lógica de negocio está prohibida en Views y Serializers.

## Inicio rápido (Docker)

```powershell
docker-compose up
```

Servidor en `http://localhost:8081`, MySQL en `localhost:3307`.

El entrypoint ejecuta automáticamente: migraciones + bootstrap del superusuario.

## Inicio rápido (local)

```powershell
# Activar entorno virtual
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (copiar example.env a .env y ajustar)

# Generar y aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario inicial
python manage.py bootstrap_admin

# Iniciar servidor de desarrollo
python manage.py runserver
```

## Variables de entorno

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DB_HOST` | Host de MySQL | `localhost` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_DATABASE` | Nombre de la BD | `teleparkbackend` |
| `DB_USER` | Usuario de MySQL | `teleparkUser` |
| `DB_PASSWORD` | Contraseña de MySQL | `teleparkUser` |
| `SECRET_KEY` | Clave secreta de Django | — |
| `SITE_URL` | URL del sitio | `http://localhost:8081` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes CSRF permitidos | `http://localhost:8080` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `ADMIN_BOOTSTRAP_PASSWORD` | Password del superusuario inicial | — |
| `ENV` | Entorno (`dev` / `prod`) | `dev` |

## API Documentation

Con `drf-spectacular`:

| Ruta | Descripción |
|---|---|
| `/api/schema/swagger-ui/` | Swagger UI interactivo |
| `/api/schema/redoc/` | ReDoc |
| `/api/schema/` | Esquema OpenAPI 3.0 (YAML) |

En `dev` son públicas; en `prod` requieren `IsAdminUser`.

## Comandos útiles

```powershell
python manage.py check                       # Validación estática
python manage.py spectacular --validate       # Validar esquema OpenAPI
python manage.py bootstrap_admin             # Crear superusuario (idempotente)
python manage.py makemigrations              # Generar migrations
python manage.py migrate                     # Aplicar migrations
```

## Estructura del proyecto

```
telepark-backend/
├── core/                  # Infraestructura compartida
├── usuarios/              # Autenticación y usuarios
├── personas/              # Módulo raíz del dominio (6 modelos)
├── salud/                 # Módulo salud (5 modelos)
├── eventos/               # Módulo eventos (2 modelos)
├── obra_social/           # Módulo obra social (2 modelos)
├── talleres/              # Módulo talleres (11 modelos)
├── telepark/              # Configuración de Django (settings, urls raíz)
├── BD/                    # Assets de diseño de base de datos
├── .specs/                # Documentación de arquitectura y procesos
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

## Convenciones

- Las FKs entre módulos usan **referencias con string**: `models.ForeignKey('personas.PersonaEp', ...)`
- No hay archivos de migración en el repositorio — se generan con `makemigrations`
- `DEBUG = True` solo cuando `ENV=dev`
- Autenticación via JWT (access token: 60 min, refresh: 1 día, `USER_ID_FIELD = 'username'`)
