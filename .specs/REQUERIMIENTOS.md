# REQUERIMIENTOS — Ciclo de Estabilización Brownfield

> **Ciclo:** CICLO-20260702-001  
> **Modo:** BROWNFIELD  
> **Baseline de referencia:** `.specs/BASELINE.md` (commit `7c3eb7c`)  
> **Objetivo exclusivo:** Estabilización del entorno — sin alteraciones funcionales en la API.

---

## Contexto del Sistema Legacy (desde BASELINE.md)

El proyecto Telepark Backend corre sobre **Django 3.2.5** (EOL desde abril 2024) con **djangorestframework 3.12.4** y base de datos MySQL. Se han detectado:

- **25 dependencias** en `requirements.txt`, de las cuales **22 están desactualizadas**, **13 son eliminables sin impacto funcional**, y **5 arrastran CVEs conocidos** (Django 3.2.5, urllib3 1.26.6, PyJWT 2.1.0).
- **Código muerto:** Archivo completo `views.py` (34 líneas, no enrutado), `admin.py` stub, `tests.py` stub.
- **Serializador duplicado:** `EnfermedadSerializer` definido dos veces en `serializers.py`.
- **django-rest-swagger** y 5 dependencias transitivas muertas no referenciadas en ningún archivo `.py`.

**Stack tecnológico actual:**
| Componente | Versión Actual | Estado | Versión Recomendada (verificada) |
|-----------|---------------|--------|----------------------------------|
| Django | 3.2.5 | 🔴 EOL (Abril 2024) | **5.2.x LTS** — compatible con Python 3.14 |
| DRF | 3.12.4 | 🟡 Desactualizado | **3.17.1** (PyPI, marzo 2026) |
| simplejwt | 4.7.2 | 🟡 Desactualizado | **5.5.1** (PyPI) |
| django-cors-headers | 3.10.1 | 🟡 Desactualizado | **4.9.0** (PyPI) |
| django-rest-swagger | 2.2.0 | 🔴 Deprecado (2019) | ❌ **ELIMINAR** |
| python-dotenv | 0.18.0 | 🟡 Desactualizado | **1.2.2** (PyPI, marzo 2026) |
| mysqlclient | 2.1.0 | 🟡 Desactualizado | **2.2.8** (PyPI, feb 2026) — wheels para cp314 ✓ |
| PyJWT | 2.1.0 | 🔴 CVE conocido | **2.13.0** (PyPI, mayo 2026) |
| urllib3 | 1.26.6 | 🔴 CVE conocido, 1.26 EOL | **2.7.0** (PyPI, mayo 2026) |
| requests | 2.26.0 | 🟡 Desactualizado | **2.34.2** (PyPI, mayo 2026) |
| certifi | 2021.5.30 | 🔴 Desactualizado | **2026.05.20** (PyPI, fecha) |
| sqlparse | 0.4.1 | 🟡 Desactualizado | **0.5.4** (PyPI) |
| asgiref | 3.4.1 | 🟡 Desactualizado | **3.11.1** (PyPI, feb 2026) |
| Jinja2 | 3.0.1 | 🟡 Desactualizado | **3.1.6** (PyPI, marzo 2025) |
| setuptools | 41.2.0 | 🔴 Obsoleto | **82.0.1** (PyPI, marzo 2026) |
| pytz | 2021.1 | 🟡 Desactualizado | Reemplazar por `zoneinfo` (stdlib Python 3.9+) |
| MarkupSafe | 2.0.1 | 🟡 Desactualizado | Actualizar con Jinja2 |
| simplejson | 3.17.3 | 🟢 Funcional | Mantener versión (no hay breaking changes) |

> **Nota:** Python **3.14.2** está instalado en el entorno de ejecución. Django 4.2 LTS solo soporta Python ≤3.12, por lo que **no es compatible**. La versión mínima de Django requerida es **5.2 LTS** (soporta Python 3.10-3.14) o **6.0.6** (soporta Python 3.12-3.14). Para un ciclo de estabilización, se recomienda **Django 5.2 LTS** por su ventana de soporte extendido.

---

## Plan de Actualización de Dependencias (Verificado con Context7 + PyPI)

> Las versiones recomendadas han sido verificadas contra las fuentes oficiales (PyPI, GitHub, documentación oficial) usando Context7 MCP y web search al 2026-07-02.

### Dependencias a ACTUALIZAR

| Paquete | Versión Actual | Versión Objetivo | Fuente de Verificación | Notas |
|---------|---------------|------------------|------------------------|-------|
| Django | 3.2.5 | **5.2.x LTS** ⚠️ | `docs.djangoproject.com` | 4.2 LTS NO compatible con Python 3.14. 5.2 LTS es la versión LTS mínima que soporta Python 3.10-3.14 |
| djangorestframework | 3.12.4 | **3.17.1** | `pypi.org/project/djangorestframework` | Soporta Django 4.2-6.0, Python ≥3.10 |
| django-cors-headers | 3.10.1 | **4.9.0** | `pypi.org/project/django-cors-headers` | Compatible con Django 4.2-6.0, Python 3.10-3.14 |
| djangorestframework-simplejwt | 4.7.2 | **5.5.1** | `pypi.org/project/djangorestframework-simplejwt` | Requiere Django ≥4.2, DRF ≥3.14, PyJWT ≥1.7.1. Verificar compatibilidad con Python 3.14 |
| mysqlclient | 2.1.0 | **2.2.8** | `pypi.org/project/mysqlclient` | Wheels para cp314-win_amd64 disponibles ✓ |
| python-dotenv | 0.18.0 | **1.2.2** | `pypi.org/project/python-dotenv` | Python ≥3.10. Breaking changes en set_key/unset_key |
| PyJWT | 2.1.0 | **2.13.0** | `pypi.org/project/PyJWT` | Soporta Python 3.14. CVE-2.1.0 corregido |
| urllib3 | 1.26.6 | **2.7.0** | `pypi.org/project/urllib3` | v1.26.x EOL (no mantenido). v2.x requiere Python ≥3.10 y OpenSSL ≥1.1.1 |
| requests | 2.26.0 | **2.34.2** | `pypi.org/project/requests` | Python ≥3.10 |
| certifi | 2021.5.30 | **2026.05.20** | `pypi.org/project/certifi` | Versionado por fecha (YYYY.MM.DD). CA bundle actualizado |
| sqlparse | 0.4.1 | **0.5.4** | `pypi.org/project/sqlparse` | Python ≥3.10 desde 0.5.x |
| asgiref | 3.4.1 | **3.11.1** | `pypi.org/project/asgiref` | Python ≥3.9 |
| Jinja2 | 3.0.1 | **3.1.6** | `pypi.org/project/Jinja2` | Security release |
| setuptools | 41.2.0 | **82.0.1** | `pypi.org/project/setuptools` | Python ≥3.9. Saltos de versión mayores — probar compatibilidad |
| MarkupSafe | 2.0.1 | **2.1.x+** | Dependencia de Jinja2 | Se actualiza junto con Jinja2 |
| charset-normalizer | 2.0.4 | **3.3.x+** | Dependencia de requests | Se actualiza junto con requests |
| idna | 3.2 | **3.7+** | Dependencia de requests | Se actualiza junto con requests |
| simplejson | 3.17.3 | **3.19.x** | `pypi.org/project/simplejson` | Actualizar si hay compatibilidad |
| pytz | 2021.1 | **❌ ELIMINAR** | — | Python 3.9+ incluye `zoneinfo` en stdlib. Django 5.2+ usa `zoneinfo` por defecto |

### Dependencias a ELIMINAR (código muerto verificado)

| Paquete | Versión Actual | Motivo | Evidencia |
|---------|---------------|--------|-----------|
| django-rest-swagger | 2.2.0 | Deprecado desde 2019. No importado en ningún `.py` | `grep -r "rest_swagger"` sin resultados |
| coreapi | 2.3.3 | Dependencia transitiva de swagger. No importado | Paquete no referenciado |
| coreschema | 0.0.4 | Dependencia transitiva de swagger. No importado | Paquete no referenciado |
| openapi-codec | 1.3.2 | Dependencia transitiva de swagger. No importado | Paquete no referenciado |
| uritemplate | 3.0.1 | Dependencia transitiva de swagger. No importado | Paquete no referenciado |
| itypes | 1.2.0 | Dependencia transitiva de swagger. No importado | Paquete no referenciado |

### Árbol de dependencias post-actualización (estimado)

```
Django 5.2.x LTS
├── asgiref 3.11.1
├── sqlparse 0.5.4
└── pytz → ELIMINADO (usa zoneinfo stdlib)
djangorestframework 3.17.1
djangorestframework-simplejwt 5.5.1
├── PyJWT 2.13.0
└── djangorestframework ≥3.14
django-cors-headers 4.9.0
mysqlclient 2.2.8
python-dotenv 1.2.2
requests 2.34.2
├── urllib3 2.7.0
├── certifi 2026.05.20
├── charset-normalizer 3.3.x
└── idna 3.7+
Jinja2 3.1.6
└── MarkupSafe 2.1.x
simplejson 3.19.x
setuptools 82.0.1
```

---

### US-01: Actualización de Django y dependencias a versiones estables y seguras

> **Como** administrador del sistema,  
> **quiero** actualizar Django y todas las dependencias del proyecto a versiones estables, seguras y con soporte activo,  
> **para** eliminar vulnerabilidades conocidas (CVEs) y garantizar la mantenibilidad del proyecto.

### US-02: Eliminación de código muerto

> **Como** desarrollador del equipo,  
> **quiero** eliminar todo el código fuente que no está siendo ejecutado por ningún endpoint,  
> **para** reducir la superficie de mantenimiento y evitar confusiones durante el desarrollo futuro.

### US-03: Eliminación de librerías sin uso

> **Como** administrador del sistema,  
> **quiero** remover de `requirements.txt` todas las dependencias que no son importadas por ningún módulo del proyecto,  
> **para** minimizar la cadena de suministro de software y reducir riesgos de seguridad por dependencias no utilizadas.

### US-04: Garantía de no regresión funcional

> **Como** desarrollador del equipo,  
> **quiero** que el sistema compile correctamente y todos los tests existentes pasen sin alteraciones tras los cambios,  
> **para** asegurar que la estabilización del entorno no introduzca regresiones en la funcionalidad existente.

---

## Criterios de Aceptación (sintaxis EARS)

### Ubiquitous (Comportamiento permanente del sistema)

- **REQ-01:** El sistema DEBE compilar sin errores tras aplicar todas las actualizaciones de dependencias y limpieza de código.
- **REQ-02:** Todos los tests existentes DEBEN ejecutarse correctamente (estado `PASSED`) sin modificación alguna de su lógica.
- **REQ-03:** Todos los endpoints activos listados en `BASELINE.md` (sección 3) DEBEN responder exactamente con la misma estructura de datos que antes de la intervención.
- **REQ-04:** El sistema DEBE utilizar únicamente versiones de paquetes con soporte activo (non-EOL) y sin CVEs públicos conocidos de severidad CRITICAL o HIGH en el momento del deploy.

### Event-driven (Comportamiento disparado por eventos)

- **REQ-05:** CUANDO se ejecute `python manage.py check --deploy`, el sistema DEBE reportar CERO errores de seguridad críticos (SECRET_KEY hardcodeada, ALLOWED_HOSTS genérico, DEBUG en producción).
- **REQ-06:** CUANDO se ejecute `pip install -r requirements.txt` en un entorno limpio, el sistema DEBE instalar sin conflictos de dependencias.
- **REQ-07:** CUANDO el pipeline de CI ejecute la suite de tests existente, todos los tests DEBEN retornar `PASSED` en el primer intento.

### State-driven (Comportamiento condicionado por estado)

- **REQ-08:** MIENTRAS la versión de Django sea 5.2 LTS o superior y DRF sea 3.14+, el sistema DEBE continuar funcionando sin requerir cambios en `models.py` (pues todos los modelos declaran `managed = False` explícitamente).
- **REQ-09:** MIENTRAS el paquete `django-rest-swagger` esté presente en `requirements.txt`, si no es importado por ningún módulo, el sistema DEBE funcionar idénticamente sin él tras su eliminación.

### Unwanted-behavior (Manejo de condiciones no deseadas)

- **REQ-10:** SI una dependencia eliminada resulta ser necesaria en tiempo de ejecución, ENTONCES el pipeline DEBE abortar con error claro indicando qué import falló y restaurar la dependencia.
- **REQ-11:** SI algún endpoint existente cambia su estructura de respuesta tras la actualización, ENTONCES el desarrollador DEBE revertir el cambio y notificar inmediatamente al orquestador.
- **REQ-12:** SI la actualización de Django requiere cambios en la configuración de `settings.py` (ej. `DEFAULT_AUTO_FIELD`, `MIDDLEWARE`), ENTONCES dichos cambios DEBEN ser explícitamente documentados y aprobados por revisión antes del merge.
- **REQ-13:** SI se detecta que la colisión de `basename='personaEp'` entre PersonaPViewSet y PersonaEPViewSet (bug B001) causa conflictos de ruta tras la actualización, ENTONCES el desarrollador DEBE corregir el basename y reportarlo explícitamente.

### Optional-feature (Comportamiento condicionado por feature opcional)

- **REQ-14:** DONDE existan múltiples versiones candidatas para la actualización de Django (5.2 LTS vs 6.0.x), el equipo DEBE optar por la versión LTS (5.2 LTS) dado que: (a) Python 3.14.2 está instalado y 5.2 LTS lo soporta oficialmente; (b) 5.2 LTS ofrece ventana de soporte extendido; (c) 6.0.x no es LTS y requeriría migración a 6.2 LTS futura.
- **REQ-15:** DONDE `django-rest-swagger` sea eliminado, DONDE la documentación de API sea requerida en el futuro, el equipo DEBE considerar `drf-spectacular` como reemplazo (no incluido en este ciclo de estabilización).

---

## Fuera de Alcance (Out of Scope)

1. ✗ **No se agregarán nuevas funcionalidades o endpoints.**
2. ✗ **No se migrará el esquema de base de datos** (modelos `managed=False` se mantienen).
3. ✗ **No se agregarán tests nuevos** más allá de los existentes.
4. ✗ **No se refactorizará la lógica de negocio** — solo limpieza de dead code y dependencias.
5. ✗ **No se reemplazará django-rest-swagger por drf-spectacular** en este ciclo (queda para ciclo futuro si se requiere documentación).
6. ✗ **No se modificará la autenticación o el modelo de usuarios** (JWT, tokens, etc.).
7. ✗ **No se cambiará el motor de base de datos** (MySQL se mantiene).
8. ✗ **No se corregirán los bugs B002 y B003** a menos que la actualización de Django/DRF los haga sintácticamente inválidos. Quedan registrados en BASELINE.md para ciclos futuros.

---

## Trazabilidad

| User Story | Criterios EARS asociados |
|-----------|-------------------------|
| US-01 | REQ-01, REQ-04, REQ-05, REQ-06, REQ-08, REQ-12, REQ-14 |
| US-02 | REQ-01, REQ-03, REQ-11 |
| US-03 | REQ-01, REQ-06, REQ-09, REQ-10, REQ-15 |
| US-04 | REQ-01, REQ-02, REQ-07, REQ-13 |

---

## Aprobación

> **Estado:** PENDIENTE DE APROBACIÓN HUMANA  
> **Pipeline bloqueado hasta:** `USER_CHECKPOINT` para confirmación del usuario.
