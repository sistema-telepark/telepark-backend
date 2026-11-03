# Telepark Backend

API REST para la gestión integral de personas, obra social, talleres, salud y eventos en el Taller de Parkinson.

## Stack

| Componente | Versión |
|---|---|
| Python | 3.14.2 |
| Django | 6.0.6 |
| Django REST Framework | 3.17.1 |
| MySQL | 8.4 |
| djangorestframework-simplejwt | 5.4.0 |
| drf-spectacular | 0.29.0 |

## Arquitectura

Monolito modular (**modulith**) con 7 apps organizadas en dos capas:

**Infraestructura interna**
- `autenticacion` — autenticación JWT, registro y gestión de usuarios (wrapper sobre `django.contrib.auth.User`)
- `core` — router central, middleware de errores, permisos, health check

**Dominio de negocio**
- `personas` — módulo raíz: personas, vínculos, direcciones, localidades
- `salud` — diagnósticos, evoluciones, enfermedades, medicamentos
- `eventos` — eventos y tipos de evento
- `obra_social` — obras sociales y coberturas
- `talleres` — talleres, clases, actividades, asistencia, observaciones

El grafo de **FKs de dominio** apunta a `personas`. Existe además una dependencia funcional de código `talleres → eventos` (justificación de ausencias), sin dependencia inversa. El grafo total de dependencias debe permanecer acíclico.

La arquitectura separa las responsabilidades en estas capas; los Services son selectivos y no se usan para CRUD sencillo:

```text
HTTP → URLs → Views/ViewSets → Serializers
                    ├─ CRUD sencillo → Managers/QuerySets → Models
                    └─ caso de uso coordinado → Services → Managers/QuerySets → Models
```

- **Views/ViewSets:** ciclo HTTP, ruteo y adaptación de la respuesta; sin reglas de negocio ni coordinación de escrituras.
- **Serializers:** validan los datos de entrada y representan la salida. Pueden implementar `create()`/`update()` y escrituras anidadas acotadas.
- **Services:** coordinan casos de uso con varios pasos, transacciones o dominios. Son código Python sin dependencia de HTTP/DRF; aceptan datos ya validados y propagan excepciones de dominio. No deben ser wrappers passthrough.
- **Managers/QuerySets:** consultas y operaciones sobre colecciones, por ejemplo filtros y orden vía `OrdenadoManager` (`core/managers.py`) y overrides por dominio (`NombreOrderedManager`, `PersonaManager`, `EncuentroManager`). Siguen siendo la capa de acceso a datos y no se reemplazan por Services.
- **Models:** invariantes y comportamiento asociados a una instancia.

La adopción de Services es gradual: se introducen para casos de uso coordinados cuando se desarrollan o refactorizan, sin reescribir de una vez los CRUD existentes.

## Inicio rápido (Docker)

```powershell
docker compose up
```

Servidor en `http://localhost:8080`, MySQL en `localhost:3306`.

El entrypoint ejecuta automáticamente: migraciones + bootstrap del superusuario.

## Inicio rápido (local)

```powershell
# Activar entorno virtual
.venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (copiar .env.example a .env y ajustar)

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
| `DB_PASSWORD` | Contraseña de MySQL | — |
| `SECRET_KEY` | Clave secreta de Django | — |
| `SITE_URL` | URL del sitio | `http://localhost:3000` |
| `CSRF_TRUSTED_ORIGINS` | Orígenes CSRF permitidos | `http://localhost:8080` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `ADMIN_BOOTSTRAP_PASSWORD` | Password del superusuario inicial | — |
| `ENV` | Entorno (`dev` / `prod`) | `dev` |

## API Documentation

Con `drf-spectacular`:

| Ruta | Descripción |
|---|---|
| `/schema/swagger-ui/` | Swagger UI interactivo |
| `/schema/redoc/` | ReDoc |
| `/schema/` | Esquema OpenAPI 3.0 (YAML) |

En `dev` son públicas; en `prod` requieren `IsAdminUser`.

## Comandos útiles

```powershell
python manage.py check                       # Validación estática
python manage.py spectacular --validate      # Validar esquema OpenAPI
python manage.py bootstrap_admin             # Crear superusuario (idempotente)
python manage.py makemigrations              # Generar migrations
python manage.py migrate                     # Aplicar migrations
```

## Estructura del proyecto

```
telepark-backend/
├── core/                  # Infraestructura compartida
├── autenticacion/         # Autenticación y usuarios
├── personas/              # Módulo raíz del dominio (8 modelos)
├── salud/                 # Módulo salud (5 modelos)
├── eventos/               # Módulo eventos (2 modelos)
├── obra_social/           # Módulo obra social (2 modelos)
├── talleres/              # Módulo talleres (11 modelos)
├── telepark/              # Configuración de Django (settings, urls raíz)
├── BD/                    # Assets de diseño de base de datos
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

## Convenciones

- Las FKs entre módulos usan **referencias con string**: `models.ForeignKey('personas.PersonaEP', ...)`
- `DEBUG = True` solo cuando `ENV=dev`
- Autenticación via JWT (access token: 60 min, refresh: 1 día, `USER_ID_FIELD = 'username'`)
