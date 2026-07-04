# ARQUITECTURA — Contrato Arquitectónico de Bounded Contexts

> **Ciclo:** CICLO-20260703-002  
> **Fecha:** 2026-07-03  
> **Modo:** BROWNFIELD  
> **Artefacto:** Contrato vinculante para división del monolito `teleparkApi` en 6 módulos (Bounded Contexts)  
> **Precedencia:** Este documento tiene precedencia sobre decisiones técnicas ad-hoc. Solo puede ser modificado mediante aprobación explícita del orquestador.

---

## Índice

1. [Stack Tecnológico](#1-stack-tecnológico)
2. [Patrón Arquitectónico](#2-patrón-arquitectónico)
3. [Topología de Módulos](#3-topología-de-módulos)
4. [Contratos de Interfaces entre Módulos](#4-contratos-de-interfaces-entre-módulos)
5. [Plan de Movimiento de Archivos](#5-plan-de-movimiento-de-archivos)
6. [Plan de Migraciones](#6-plan-de-migraciones)
7. [Plan de Configuración (settings.py)](#7-plan-de-configuración-settingspy)
8. [Riesgos y Mitigaciones](#8-riesgos-y-mitigaciones)
9. [Contrato Vinculante](#9-contrato-vinculante)

---

## 1. Stack Tecnológico

### 1.1. Stack Confirmado (sin cambios respecto al ciclo anterior)

| Componente | Versión | Nota |
|-----------|---------|-------|
| **Python** | 3.14.2 | Sin cambios |
| **Django** | 6.0.6 | Sin cambios |
| **djangorestframework** | 3.17.1 | Sin cambios |
| **djangorestframework-simplejwt** | 5.5.1 | Sin cambios |
| **mysqlclient** | 2.2.8 | Sin cambios |
| **django-cors-headers** | 4.9.0 | Sin cambios |
| **MySQL Server** | 8.0.x | Sin cambios |
| **Docker / Docker Compose** | ≥ 24.0 / ≥ 2.20 | Sin cambios |

### 1.2. Cambios en requirements.txt
Ninguno. La división en módulos es puramente estructural, no agrega ni modifica dependencias.

---

## 2. Patrón Arquitectónico

### 2.1. Estrategia: Modular Monolith (Monolito Modular)

Se adopta el patrón **Monolito Modular** (también conocido como *Modulith*):
- **Un solo proceso Django** — todos los módulos se despliegan juntos
- **Una sola base de datos MySQL** — todos los módulos comparten la misma BD
- **Módulos como Django apps independientes** — cada contexto es una Django app con su propio `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py`
- **Comunicación entre módulos** — vía importación directa de servicios o modelos (misma BD, sin necesidad de API calls HTTP internas)
- **Fronteras explícitas** — cada módulo declara sus dependencias en `apps.py`

### 2.2. Principios de Diseño

| Principio | Aplicación |
|-----------|-----------|
| **Alta cohesión** | Cada módulo agrupa modelos que pertenecen al mismo concepto de dominio |
| **Bajo acoplamiento** | Las FK entre módulos usan string-based references (`'app_label.ModelName'`) |
| **Sin dependencias circulares** | El grafo de dependencias es un DAG (ver sección 3) |
| **Encapsulamiento** | Cada módulo expone serializadores y servicios, no los modelos directamente |
| **Preservación de API pública** | Todos los endpoints REST existentes mantienen exactamente las mismas rutas y respuestas |

---

## 3. Topología de Módulos

### 3.1. Mapa Completo

```
telepark-backend/
├── telepark/                  (proyecto Django — settings, root urls)
├── core/                      (infraestructura compartida — SIN MODELOS)
├── personas/                  (contexto raíz)
├── salud/                     → personas
├── eventos/                   → personas
├── obra_social/               → personas
├── talleres/                  → personas
├── teleparkApi/               (🚫 se elimina como app — queda como carpeta residual o se limpia)
└── manage.py
```

### 3.2. Distribución de Modelos por Módulo

| Módulo (app_label) | Modelos | db_table | ¿Tiene FK a otro módulo? |
|-------------------|---------|----------|--------------------------|
| **personas** | Persona | `persona` | ❌ (personas → Direccion, todo intrazona) |
| | PersonaEp | `persona_ep` | ❌ (PersonaEp → Persona, intrazona) |
| | Direccion | `direccion` | ❌ (Direccion → Localidad, intrazona) |
| | Localidad | `localidad` | ❌ (Localidad → Municipio, intrazona) |
| | Municipio | `municipio` | ❌ (standalone) |
| | Tipoparentesco | `tipoparentesco` | ❌ (Tipoparentesco → Persona+PersonaEp, intrazona) |
| **salud** | Diagnostico | `diagnostico` | ✅ → personas.PersonaEp |
| | Evolucion | `evolucion` | ✅ → personas.PersonaEp |
| | Enfermedad | `enfermedad` | ❌ (standalone) |
| | Medicamento | `medicamento` | ❌ (standalone) |
| | Indicacionmedicamento | `indicacionmedicamento` | ✅ → personas.PersonaEp, salud.Medicamento |
| **eventos** | Evento | `evento` | ✅ → personas.PersonaEp, eventos.Tipoevento |
| | Tipoevento | `tipoevento` | ❌ (standalone) |
| **obra_social** | Obrasocial | `obrasocial` | ❌ (standalone) |
| | Os | `os` | ✅ → personas.PersonaEp, obra_social.Obrasocial |
| **talleres** | Taller | `taller` | ❌ (standalone) |
| | Clasetaller | `clasetaller` | ✅ → talleres.Taller |
| | Actividad | `actividad` | ✅ → talleres.Taller |
| | Actividadrealizada | `actividadrealizada` | ✅ → talleres.Actividad, talleres.Clasetaller |
| | Asistenciataller | `asistenciataller` | ✅ → **personas.PersonaEp**, talleres.Clasetaller, talleres.Comportamiento |
| | Comportamiento | `comportamiento` | ❌ (standalone) |
| | Factorclase | `factorclase` | ✅ → talleres.Clasetaller, talleres.Factorglobal |
| | Factorglobal | `factorglobal` | ❌ (standalone) |
| | Unidadobservacion | `unidadobservacion` | ❌ (standalone) |
| | Variableuo | `variableuo` | ✅ → talleres.Comportamiento, talleres.Unidadobservacion |
| | Valorvariableuo | `valorvariableuo` | ✅ → talleres.Variableuo |
| **core** | _(ninguno)_ | — | — |

### 3.3. Grafo de Dependencias (DAG)

```
core ──→ (ninguno)               ← plano, helpers/infra
personas ──→ (ninguno)           ← raíz del dominio
salud ──→ personas               ← Diagnostico/Evolucion/Indicacion → PersonaEp
eventos ──→ personas             ← Evento → PersonaEp
obra_social ──→ personas         ← Os → PersonaEp
talleres ──→ personas            ← Asistenciataller → PersonaEp
```

**✅ No hay ciclos.** Todas las FK externas apuntan exclusivamente a `personas`.

### 3.4. Distribución de Archivos de Código

#### 3.4.1. Módulo `core` (infraestructura compartida)

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `core/__init__.py` | 🆕 Nuevo | Paquete |
| `core/apps.py` | 🆕 Nuevo | `CoreConfig`, `name='core'` |
| `core/authentication.py` | ← `teleparkApi/authentication.py` | Importa helpers, permission, static |
| `core/helpers.py` | ← `teleparkApi/helpers.py` | |
| `core/middleware.py` | ← `teleparkApi/middleware.py` | |
| `core/permission.py` | ← `teleparkApi/permission.py` | |
| `core/static.py` | ← `teleparkApi/static.py` | |
| `core/views.py` | 🆕 Nuevo | Solo `health_check()` |
| `core/urls.py` | 🆕 Nuevo | Router central que agrega rutas de todos los módulos + auth |

#### 3.4.2. Módulo `personas`

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `personas/__init__.py` | 🆕 Nuevo | |
| `personas/apps.py` | 🆕 Nuevo | `PersonasConfig`, `name='personas'` |
| `personas/models.py` | ← `teleparkApi/models.py` (6 modelos) | Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco |
| `personas/services.py` | ← `teleparkApi/services.py` (6 clases) | PersonaService, PersonaEpService, DireccionService, TipoParentescoService, LocalidadService, MunicipioService |
| `personas/serializers.py` | ← `teleparkApi/serializers.py` (7 serializers) | PersonaSerializer, PersonaEpSerializer, PersonaPSerializer, DireccionSerializer, LocalidadSerializer, MunicipioSerializer, TipoparentescoSerializer |
| `personas/views.py` | ← `teleparkApi/views.py` (7 ViewSets) | PersonaViewSet, PersonaEPViewSet, PersonaPViewSet, LocalidadViewSet, DireccionViewSet, TipoParentescoViewSet, MunicipioViewSet |
| `personas/urls.py` | 🆕 Nuevo | Router con las 7 rutas de personas |
| `personas/migrations/` | 🆕 Nuevo | Migraciones para personas |

#### 3.4.3. Módulo `salud`

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `salud/__init__.py` | 🆕 Nuevo | |
| `salud/apps.py` | 🆕 Nuevo | `SaludConfig`, `name='salud'` |
| `salud/models.py` | ← `teleparkApi/models.py` (5 modelos) | Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento |
| `salud/services.py` | ← `teleparkApi/services.py` (5 clases) | DiagnosticoService, EvolucionService, EnfermedadService, MedicamentoService, IndicacionService |
| `salud/serializers.py` | ← `teleparkApi/serializers.py` (6 serializers) | DiagnosticoSerializer, DiagnosticoEpSerializer, EvolucionSerializer, EnfermedadSerializer, MedicamentoSerializer, IndicacionSerializer, IndicacionEpSerializer |
| `salud/views.py` | ← `teleparkApi/views.py` (5 ViewSets) | DiagnosticoViewSet, EvolucionViewSet, EnfermedadViewSet, MedicamentoViewSet, IndicacionViewSet |
| `salud/urls.py` | 🆕 Nuevo | Router con las 5 rutas de salud |
| `salud/migrations/` | 🆕 Nuevo | Migraciones para salud |

#### 3.4.4. Módulo `eventos`

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `eventos/__init__.py` | 🆕 Nuevo | |
| `eventos/apps.py` | 🆕 Nuevo | `EventosConfig`, `name='eventos'` |
| `eventos/models.py` | ← `teleparkApi/models.py` (2 modelos) | Evento, Tipoevento |
| `eventos/services.py` | ← `teleparkApi/services.py` (2 clases) | EventoService, TipoEventoService |
| `eventos/serializers.py` | ← `teleparkApi/serializers.py` (2 serializers) | EventoSerializer, TipoEventoSerializer |
| `eventos/views.py` | ← `teleparkApi/views.py` (2 ViewSets) | EventoViewSet, TipoEventoViewSet |
| `eventos/urls.py` | 🆕 Nuevo | Router con las 2 rutas de eventos |
| `eventos/migrations/` | 🆕 Nuevo | Migraciones para eventos |

#### 3.4.5. Módulo `obra_social`

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `obra_social/__init__.py` | 🆕 Nuevo | |
| `obra_social/apps.py` | 🆕 Nuevo | `ObraSocialConfig`, `name='obra_social'` |
| `obra_social/models.py` | ← `teleparkApi/models.py` (2 modelos) | Obrasocial, Os |
| `obra_social/services.py` | ← `teleparkApi/services.py` (2 clases) | ObraSocialService, OsService |
| `obra_social/serializers.py` | ← `teleparkApi/serializers.py` (3 serializers) | ObraSocialSerializer, OSSerializer, OSEpSerializer |
| `obra_social/views.py` | ← `teleparkApi/views.py` (2 ViewSets) | ObraSocialViewSet, OSViewSet |
| `obra_social/urls.py` | 🆕 Nuevo | Router con las 2 rutas de obra_social |
| `obra_social/migrations/` | 🆕 Nuevo | Migraciones para obra_social |

#### 3.4.6. Módulo `talleres`

| Archivo destino | Origen | Notas |
|----------------|--------|-------|
| `talleres/__init__.py` | 🆕 Nuevo | |
| `talleres/apps.py` | 🆕 Nuevo | `TalleresConfig`, `name='talleres'` |
| `talleres/models.py` | ← `teleparkApi/models.py` (11 modelos) | Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo |
| `talleres/services.py` | 🆕 Nuevo | Servicios CRUD básicos para los modelos que no tenían (ver sección 3.5) |
| `talleres/serializers.py` | 🆕 Nuevo | Serializers básicos para los 11 modelos |
| `talleres/views.py` | 🆕 Nuevo | ViewSets básicos para los 11 modelos |
| `talleres/urls.py` | 🆕 Nuevo | Router con rutas de talleres |
| `talleres/migrations/` | 🆕 Nuevo | Migraciones para talleres |

### 3.5. Servicios Faltantes — Talleres (REQ-22)

Actualmente los 11 modelos de `talleres` NO tienen servicios, serializadores ni vistas. Como parte de este ciclo (opcional, REQ-22), se propone crear:

| Modelo | Servicio | Serializador | ViewSet |
|--------|----------|-------------|---------|
| Taller | TallerService (BaseService) | TallerSerializer | TallerViewSet |
| Clasetaller | ClaseTallerService (BaseService) | ClaseTallerSerializer | ClaseTallerViewSet |
| Actividad | ActividadService (BaseService) | ActividadSerializer | ActividadViewSet |
| Actividadrealizada | ActividadRealizadaService (BaseService) | ActividadRealizadaSerializer | ActividadRealizadaViewSet |
| Asistenciataller | AsistenciaTallerService (BaseService) | AsistenciaTallerSerializer | AsistenciaTallerViewSet |
| Comportamiento | ComportamientoService (BaseService) | ComportamientoSerializer | ComportamientoViewSet |
| Factorclase | FactorClaseService (BaseService) | FactorClaseSerializer | FactorClaseViewSet |
| Factorglobal | FactorGlobalService (BaseService) | FactorglobalSerializer | FactorGlobalViewSet |
| Unidadobservacion | UnidadObservacionService (BaseService) | UnidadObservacionSerializer | UnidadObservacionViewSet |
| Variableuo | VariableUOService (BaseService) | VariableUOSerializer | VariableUOViewSet |
| Valorvariableuo | ValorVariableUOService (BaseService) | ValorVariableUOSerializer | ValorVariableUOViewSet |

> **Importante:** Los endpoints de talleres se registrarán bajo el prefijo `api/` para mantener consistencia.

---

## 4. Contratos de Interfaces entre Módulos

### 4.1. Referencias FK entre módulos

Todas las FK que cruzan fronteras de módulo DEBEN usar la sintaxis `'app_label.ModelName'` como string:

| Módulo Origen | Modelo | Campo FK | Destino (app.Model) |
|--------------|--------|----------|---------------------|
| salud | Diagnostico | `idpersonaep` | `'personas.PersonaEp'` |
| salud | Evolucion | `idpersonaep` | `'personas.PersonaEp'` |
| salud | Indicacionmedicamento | `idpersonaep` | `'personas.PersonaEp'` |
| eventos | Evento | `idpersonaep` | `'personas.PersonaEp'` |
| obra_social | Os | `idpersonaep` | `'personas.PersonaEp'` |
| talleres | Asistenciataller | `idpersonaep` | `'personas.PersonaEp'` |

### 4.2. Serializadores — Anidaciones entre módulos

Se identificaron **0 anidaciones cross-module**. Todos los serializadores que referencian otros serializadores lo hacen dentro del mismo módulo en la nueva topología:

| Serializer | Anida a | ¿Mismo módulo? |
|-----------|---------|----------------|
| PersonaPSerializer (personas) | PersonaSerializer (personas) | ✅ |
| DiagnosticoEpSerializer (salud) | EnfermedadSerializer (salud) | ✅ |
| EventoSerializer (eventos) | TipoEventoSerializer (eventos) | ✅ |
| OSEpSerializer (obra_social) | ObraSocialSerializer (obra_social) | ✅ |
| IndicacionEpSerializer (salud) | MedicamentoSerializer (salud) | ✅ |

### 4.3. Servicios — Dependencias entre módulos

Los servicios de cada módulo importan modelos **exclusivamente de su propio módulo**. No hay servicios que crucen fronteras de módulo. Los ViewSets importan servicios de su propio módulo.

**Excepción:** Los `@action` endpoints (`filtrar_por_persona()`) devuelven datos que serializan modelos de `personas` (PersonaEp) indirectamente, pero la serialización se hace dentro del ViewSet que llama al servicio local.

### 4.4. URLs — Mapeo de Endpoints

| Ruta Actual (monolito) | Ruta Final (modular) | ViewSet | Módulo |
|-----------------------|---------------------|---------|--------|
| `/api/persona` | `/api/persona` | PersonaViewSet | personas |
| `/api/personaEp` | `/api/personaEp` | PersonaEPViewSet | personas |
| `/api/personaP` | `/api/personaP` | PersonaPViewSet | personas |
| `/api/direccion` | `/api/direccion` | DireccionViewSet | personas |
| `/api/tipoparentesco` | `/api/tipoparentesco` | TipoParentescoViewSet | personas |
| `/api/localidad` | `/api/localidad` | LocalidadViewSet | personas |
| `/api/municipio` | `/api/municipio` | MunicipioViewSet | personas |
| `/api/diagnostico` | `/api/diagnostico` | DiagnosticoViewSet | salud |
| `/api/evolucion` | `/api/evolucion` | EvolucionViewSet | salud |
| `/api/enfermedad` | `/api/enfermedad` | EnfermedadViewSet | salud |
| `/api/medicamento` | `/api/medicamento` | MedicamentoViewSet | salud |
| `/api/indicacion` | `/api/indicacion` | IndicacionViewSet | salud |
| `/api/evento` | `/api/evento` | EventoViewSet | eventos |
| `/api/tipoevento` | `/api/tipoevento` | TipoEventoViewSet | eventos |
| `/api/obrasocial` | `/api/obrasocial` | ObraSocialViewSet | obra_social |
| `/api/os` | `/api/os` | OSViewSet | obra_social |
| `/api/login` | `/api/login` | auth_view | core |
| `/api/create_user` | `/api/create_user` | create_user | core |
| `/api/users` | `/api/users` | get_users | core |
| `/api/update_user` | `/api/update_user` | update_user | core |
| `/api/refresh_token` | `/api/refresh_token` | TokenRefreshView | core |
| `/api/health` | `/api/health` | health_check | core |

**📌 Todas las rutas se mantienen exactamente igual.** No hay cambios visibles para los clientes de la API.

---

## 5. Plan de Movimiento de Archivos

### 5.1. Fase 1: Crear estructura de módulos

```
Crear directorios:
  core/
  core/migrations/        (con __init__.py)
  personas/
  personas/migrations/    (con __init__.py)
  salud/
  salud/migrations/       (con __init__.py)
  eventos/
  eventos/migrations/     (con __init__.py)
  obra_social/
  obra_social/migrations/ (con __init__.py)
  talleres/
  talleres/migrations/    (con __init__.py)
```

### 5.2. Fase 2: Mover archivos de código

#### 5.2.1. Módulo core (7 archivos movidos + 3 nuevos)
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `core/__init__.py` |
| 🆕 CREAR | `core/apps.py` — `CoreConfig(name='core')` |
| 📦 COPIAR + ADAPTAR | `core/authentication.py` (cambiar imports: `.helpers` → `core.helpers`, `.permission` → `core.permission`, `.static` → `core.static`) |
| 📦 COPIAR | `core/helpers.py` (sin cambios) |
| 📦 COPIAR | `core/middleware.py` (sin cambios) |
| 📦 COPIAR | `core/permission.py` (sin cambios) |
| 📦 COPIAR | `core/static.py` (sin cambios) |
| 🆕 CREAR | `core/views.py` — extraer `health_check` de `teleparkApi/views.py` |
| 🆕 CREAR | `core/urls.py` — router central que unifica las rutas de todos los módulos + auth |

#### 5.2.2. Módulo personas
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `personas/__init__.py` |
| 🆕 CREAR | `personas/apps.py` — `PersonasConfig(name='personas')` |
| 📦 COPIAR (6 modelos) | `personas/models.py` — Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco |
| 📦 COPIAR (6 servicios) | `personas/services.py` — PersonaService, PersonaEpService, DireccionService, TipoParentescoService, LocalidadService, MunicipioService |
| 📦 COPIAR (7 serializers) | `personas/serializers.py` — PersonaSerializer, PersonaEpSerializer, PersonaPSerializer, DireccionSerializer, LocalidadSerializer, MunicipioSerializer, TipoparentescoSerializer |
| 📦 COPIAR (7 ViewSets) | `personas/views.py` — PersonaViewSet, PersonaEPViewSet, PersonaPViewSet, LocalidadViewSet, DireccionViewSet, TipoParentescoViewSet, MunicipioViewSet |
| 🆕 CREAR | `personas/urls.py` — router con registros para las 7 rutas de personas |

#### 5.2.3. Módulo salud
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `salud/__init__.py` |
| 🆕 CREAR | `salud/apps.py` — `SaludConfig(name='salud')` |
| 📦 COPIAR (5 modelos) | `salud/models.py` — Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento |
| 📦 COPIAR (5 servicios) | `salud/services.py` — DiagnosticoService, EvolucionService, EnfermedadService, MedicamentoService, IndicacionService |
| 📦 COPIAR (7 serializers) | `salud/serializers.py` — DiagnosticoSerializer, DiagnosticoEpSerializer, EvolucionSerializer, EnfermedadSerializer, MedicamentoSerializer, IndicacionSerializer, IndicacionEpSerializer |
| 📦 COPIAR (5 ViewSets) | `salud/views.py` — DiagnosticoViewSet, EvolucionViewSet, EnfermedadViewSet, MedicamentoViewSet, IndicacionViewSet |
| 🆕 CREAR | `salud/urls.py` — router con registros para las 5 rutas de salud |

#### 5.2.4. Módulo eventos
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `eventos/__init__.py` |
| 🆕 CREAR | `eventos/apps.py` — `EventosConfig(name='eventos')` |
| 📦 COPIAR (2 modelos) | `eventos/models.py` — Evento, Tipoevento |
| 📦 COPIAR (2 servicios) | `eventos/services.py` — EventoService, TipoEventoService |
| 📦 COPIAR (2 serializers) | `eventos/serializers.py` — EventoSerializer, TipoEventoSerializer |
| 📦 COPIAR (2 ViewSets) | `eventos/views.py` — EventoViewSet, TipoEventoViewSet |
| 🆕 CREAR | `eventos/urls.py` — router con registros para las 2 rutas de eventos |

#### 5.2.5. Módulo obra_social
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `obra_social/__init__.py` |
| 🆕 CREAR | `obra_social/apps.py` — `ObraSocialConfig(name='obra_social')` |
| 📦 COPIAR (2 modelos) | `obra_social/models.py` — Obrasocial, Os |
| 📦 COPIAR (2 servicios) | `obra_social/services.py` — ObraSocialService, OsService |
| 📦 COPIAR (3 serializers) | `obra_social/serializers.py` — ObraSocialSerializer, OSSerializer, OSEpSerializer |
| 📦 COPIAR (2 ViewSets) | `obra_social/views.py` — ObraSocialViewSet, OSViewSet |
| 🆕 CREAR | `obra_social/urls.py` — router con registros para las 2 rutas de obra_social |

#### 5.2.6. Módulo talleres
| Acción | Archivo |
|--------|---------|
| 🆕 CREAR | `talleres/__init__.py` |
| 🆕 CREAR | `talleres/apps.py` — `TalleresConfig(name='talleres')` |
| 📦 COPIAR (11 modelos) | `talleres/models.py` — Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo |
| 🆕 CREAR | `talleres/services.py` — 11 servicios CRUD básicos |
| 🆕 CREAR | `talleres/serializers.py` — 11 serializers básicos |
| 🆕 CREAR | `talleres/views.py` — 11 ViewSets básicos con IsAuthenticated |
| 🆕 CREAR | `talleres/urls.py` — router con 11 rutas de talleres |

### 5.3. Fase 3: Actualizar configuraciones

| Archivo | Cambio |
|---------|--------|
| `telepark/settings.py` | Reemplazar `'teleparkApi'` por `'core', 'personas', 'salud', 'eventos', 'obra_social', 'talleres'` en INSTALLED_APPS |
| `telepark/settings.py` | Cambiar middleware `teleparkApi.middleware.ExceptionMiddleware` → `core.middleware.ExceptionMiddleware` |
| `telepark/urls.py` | Cambiar `include('teleparkApi.urls')` → `include('core.urls')` |

### 5.4. Fase 4: Adaptar imports dentro de cada módulo

Los adaptadores de import necesarios son:

| Archivo | Cambio de import |
|---------|-----------------|
| `core/authentication.py` | `.helpers` → `core.helpers`, `.permission` → `core.permission`, `.static` → `core.static` |
| `salud/models.py` | `idpersonaep = ForeignKey('personas.PersonaEp', ...)` en los 3 modelos que referencian PersonaEp |
| `eventos/models.py` | `idpersonaep = ForeignKey('personas.PersonaEp', ...)` en Evento |
| `obra_social/models.py` | `idpersonaep = ForeignKey('personas.PersonaEp', ...)` en Os |
| `talleres/models.py` | `idpersonaep = ForeignKey('personas.PersonaEp', ...)` en Asistenciataller |
| `core/urls.py` | Importar routers de todos los módulos y agregar auth y health |
| `talleres/services.py` | Importar modelos desde `talleres.models` |
| `talleres/serializers.py` | Importar modelos desde `talleres.models` |
| `talleres/views.py` | Importar servicios y serializers desde `talleres` |
| `personas/serializers.py` | Importar modelos desde `personas.models` |
| `personas/views.py` | Importar servicios desde `personas.services`, serializers desde `personas.serializers` |
| (cada módulo análogamente) | Idem patrones |

### 5.5. Fase 5: Limpiar archivos fuente originales

Una vez que todo funcione:
| Archivo | Acción |
|---------|--------|
| `teleparkApi/services.py` | 🗑️ Eliminar (contenido distribuido en los 6 módulos) |
| `teleparkApi/views.py` | 🗑️ Eliminar (contenido distribuido en los 6 módulos) |
| `teleparkApi/serializers.py` | 🗑️ Eliminar (contenido distribuido en los 6 módulos) |
| `teleparkApi/urls.py` | 🗑️ Eliminar (reemplazado por `core/urls.py`) |
| `teleparkApi/authentication.py` | 🗑️ Eliminar (movido a `core/`) |
| `teleparkApi/helpers.py` | 🗑️ Eliminar (movido a `core/`) |
| `teleparkApi/middleware.py` | 🗑️ Eliminar (movido a `core/`) |
| `teleparkApi/permission.py` | 🗑️ Eliminar (movido a `core/`) |
| `teleparkApi/static.py` | 🗑️ Eliminar (movido a `core/`) |
| `teleparkApi/models.py` | 🗑️ Eliminar (distribuido en 5 módulos) |
| `teleparkApi/migrations/` | 🗑️ Eliminar (se regenerarán) |
| `teleparkApi/apps.py` | 🗑️ Eliminar (ya no es una app registrada) |
| `teleparkApi/__init__.py` | 🗑️ Eliminar (opcional) |

---

## 6. Plan de Migraciones

### 6.1. Estrategia

Al igual que en el ciclo de dockerización, se adopta la estrategia de **regenerar migraciones desde cero**:

1. **Eliminar** `teleparkApi/migrations/0001_initial.py`
2. Agregar los 6 módulos a `INSTALLED_APPS`
3. Ejecutar `python manage.py makemigrations` → genera migraciones para cada módulo
4. Ejecutar `python manage.py migrate` → aplica migraciones

### 6.2. Consideraciones

- Dado que la BD actual (Docker) fue creada con `managed=True` en el ciclo anterior, las tablas ya existen. Django usará `--fake-initial` implícitamente si detecta que las tablas ya existen con la misma estructura.
- Al cambiar los modelos de módulo, Django asignará nuevas tablas de migraciones (`django_migrations`) por cada módulo.
- Las FK string-based (`'personas.PersonaEp'`) se resuelven en tiempo de migración correctamente porque Django ya conoce todas las apps registradas.

### 6.3. Orden de migraciones

Django procesará las apps en el orden definido en `INSTALLED_APPS`:
1. `django.contrib` apps (auth, contenttypes, etc.)
2. `corsheaders`
3. `rest_framework`
4. `core` (sin modelos — ejecuta pero no crea tablas)
5. **`personas`** (primero — no tiene dependencias externas)
6. **`salud`** (depende de personas)
7. **`eventos`** (depende de personas)
8. **`obra_social`** (depende de personas)
9. **`talleres`** (depende de personas)

---

## 7. Plan de Configuración (settings.py)

### 7.1. Nuevo INSTALLED_APPS

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    # Módulos del dominio (ordenados por dependencias)
    'core',
    'personas',       # raíz — sin dependencias
    'salud',          # → personas
    'eventos',        # → personas
    'obra_social',    # → personas
    'talleres',       # → personas
]
```

### 7.2. Nuevo MIDDLEWARE

```python
MIDDLEWARE = [
    ...
    'core.middleware.ExceptionMiddleware',
]
```

### 7.3. Nueva estructura de urls.py

**telepark/urls.py:**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

---

## 8. Riesgos y Mitigaciones

### 8.1. Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Mitigación |
|----|--------|-------------|---------|------------|
| R001 | **FK con string-based reference mal escrita** | Baja | Alto — `migrate` falla | Usar exactamente `'app_label.ModelName'`. Verificar que `app_label` coincide con `name` en `apps.py` |
| R002 | **Import circular si un módulo importa a otro incorrectamente** | Baja | Alto — servidor no arranca | Seguir el DAG estrictamente. Ningún módulo importa de `salud`, `eventos`, `obra_social` o `talleres` |
| R003 | **Migraciones conflictivas con tabla existente** | Media | Medio — `migrate` falla | Usar `python manage.py migrate --fake-initial` si las tablas ya existen |
| R004 | **Serializers/Views importan modelos desde el módulo equivocado** | Media | Medio — error de import | Cada módulo importa modelos solo de su propio `models.py`. Los FKs string-based no necesitan import |
| R005 | **URLs duplicadas o conflictos de rutas** | Baja | Medio — 404 o 500 | El router central en `core/urls.py` unifica todos los prefijos `/api/...` sin superposición |
| R006 | **Caché de Python (__pycache__) con imports antiguos** | Alta | Bajo — errores confusos | Limpiar `__pycache__` de `teleparkApi/` después del movimiento |

### 8.2. Plan de Contingencia (Rollback)

Si `python manage.py check` falla después del movimiento:

```bash
# Restaurar archivos originales
git checkout -- teleparkApi/
git checkout -- telepark/settings.py
git checkout -- telepark/urls.py

# Limpiar módulos nuevos
rm -rf core/ personas/ salud/ eventos/ obra_social/ talleres/
```

---

## 9. Contrato Vinculante

### 9.1. Cláusulas Técnicas

1. **Los 26 modelos se distribuyen** en 5 módulos de dominio exactamente según la sección 3.2. Ningún modelo se duplica, elimina o modifica.
2. **Todas las FK entre módulos** usan string-based references (`'app_label.ModelName'`), nunca import directo de clase.
3. **El grafo de dependencias es un DAG**: personas → (ninguno). Los demás → personas. No hay ciclos.
4. **Las rutas de API no cambian** — todos los endpoints existentes mantienen su path exacto.
5. **Los serializers anidados** intra-módulo se mantienen. No hay anidaciones cross-módulo.
6. **Los archivos `teleparkApi/`** se eliminan después de verificar que el nuevo sistema funciona.
7. **El health_check** se mueve a `core/views.py`.
8. **La autenticación** (JWT, login, create_user, etc.) se mueve a `core/authentication.py` con imports adaptados.

### 9.2. Cláusulas de Proceso

1. **El movimiento se ejecuta en fases:** 1 (estructura) → 2 (código) → 3 (settings) → 4 (imports) → 5 (limpieza).
2. **Cada fase debe pasar `python manage.py check`** antes de avanzar a la siguiente.
3. **No se modifican modelos, lógica de negocio, ni serializadores existentes.** Solo se mueven archivos y se adaptan imports.
4. **Para los modelos de talleres**, se crean servicios/serializers/views básicos (CRUD) como parte del ciclo (REQ-22).
5. **La verificación final** es: `python manage.py check` → 0 errores + `python manage.py test` → 0 errores de importación.
6. **NINGÚN archivo se mueve hasta que el humano apruebe este plan.**

### 9.3. Cobertura de Requerimientos

| User Story | Criterios EARS | Cobertura Arquitectónica |
|------------|---------------|--------------------------|
| **US-01 — personas** | REQ-01, REQ-02, REQ-13 | Sección 3.4.2 + 5.2.2 |
| **US-02 — obra_social** | REQ-03, REQ-04, REQ-15, REQ-17 | Sección 3.4.5 + 5.2.5 + 4.1 |
| **US-03 — eventos** | REQ-05, REQ-06, REQ-15, REQ-17 | Sección 3.4.4 + 5.2.4 + 4.1 |
| **US-04 — talleres** | REQ-07, REQ-08, REQ-15, REQ-17 | Sección 3.4.6 + 5.2.6 + 4.1 |
| **US-05 — salud** | REQ-09, REQ-10, REQ-15, REQ-17 | Sección 3.4.3 + 5.2.3 + 4.1 |
| **US-06 — core** | REQ-11 | Sección 3.4.1 + 5.2.1 |
| **US-07 — sin ciclos** | REQ-12, REQ-21 | Sección 3.3 — DAG validado |
| **US-08 — sin regresiones** | REQ-14, REQ-16, REQ-18, REQ-20 | Sección 4.4 + 6 |

### 9.4. Exclusiones Explícitas

- ✗ Modificación de campos, tipos de dato, o relaciones en modelos
- ✗ Cambio en lógica de negocio de servicios o views existentes
- ✗ Implementación de event bus o mensajería entre contextos
- ✗ Cambios en autenticación (A003, B004 quedan para ciclo futuro)
- ✗ Agregar tests unitarios nuevos
- ✗ Separación de base de datos por módulo
- ✗ Dockerizar módulos por separado

---

## Aprobación

| Rol | Estado | Fecha |
|-----|--------|-------|
| **Arquitecto** (emisor) | ✅ FIRMADO | 2026-07-03 |
| **Gatekeeper (DISEÑO)** | ✅ APROBADO | 2026-07-03 |
| **Aprobación humana** | ✅ APROBADO | 2026-07-03 |

> **Pipeline:** ✅ COMPLETADO — 6 módulos implementados, 0 errores `check`.
> **Verificación final:** `python manage.py check` → 0 errores. 26 modelos en 5 módulos + core. 27 ViewSets. 5 FKs cross-module string-based.

---

## 10. ANEXO — Integración Swagger/OpenAPI (CICLO-20260704-001)

> **Ciclo:** CICLO-20260704-001
> **Fecha:** 2026-07-04
> **Propósito:** Integrar `drf-spectacular==0.29.0` para generar documentación OpenAPI 3.0 automática de todos los endpoints, manteniendo las rutas intactas.

### 10.1. Stack Modificado

| Componente | Versión | Acción |
|-----------|---------|--------|
| **drf-spectacular** | **0.29.0** | 🆕 Agregar — generador OpenAPI 3.0 para DRF |
| **PyYAML** | ≥6.0 | 🆕 Dependencia transitiva de drf-spectacular |

**Stack existente no modificado:** Python 3.14.2, Django 6.0.6, DRF 3.17.1, simplejwt, mysqlclient, django-cors-headers, etc.

### 10.2. Configuración en settings.py

```python
INSTALLED_APPS += [
    'drf_spectacular',
]

REST_FRAMEWORK['DEFAULT_SCHEMA_CLASS'] = 'drf_spectacular.openapi.AutoSchema'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Telepark API',
    'DESCRIPTION': 'API REST del sistema Telepark — módulos: personas, salud, eventos, obra_social, talleres',
    'VERSION': '1.0.0',
    'CONTACT': {'email': 'admin@telepark.com'},
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SERVE_INCLUDE_SCHEMA': False,
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'] if DEBUG else ['rest_framework.permissions.IsAdminUser'],
    'SECURITY': [{'BearerAuth': []}],
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
        'deepLinking': True,
    },
}
```

### 10.3. Nuevas rutas en core/urls.py

Se agregan 3 rutas nuevas bajo el prefijo `/api/schema/`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # ... rutas existentes ...
    
    # Documentación OpenAPI / Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

### 10.4. Dependencia en requirements.txt

```
drf-spectacular==0.29.0
```

### 10.5. Endpoints de documentación

| Ruta | Vista | Propósito | Auth (DEBUG) | Auth (Producción) |
|------|-------|-----------|:------------:|:-----------------:|
| `GET /api/schema/` | SpectacularAPIView | Esquema OpenAPI 3.0 (YAML) | ❌ Público | 🔒 IsAdminUser |
| `GET /api/schema/swagger-ui/` | SpectacularSwaggerView | UI Swagger interactiva | ❌ Público | 🔒 IsAdminUser |
| `GET /api/schema/redoc/` | SpectacularRedocView | UI ReDoc legible | ❌ Público | 🔒 IsAdminUser |

### 10.6. Seguridad (GLOBAL_RULES.md compliance)

| Regla Global | Implementación |
|-------------|----------------|
| §2.3 IAM / JWT | Security scheme `BearerAuth` configurado en `SPECTACULAR_SETTINGS.SECURITY`. Todos los endpoints protegidos muestran candado en Swagger UI. Botón "Authorize" preconfigurado para JWT Bearer. |
| §2.4 Protección de datos | El schema solo expone tipos y estructuras de serializadores — NO datos reales ni PII. |
| §2.5 Logging sanitizado | Los endpoints de documentación no logean requests. Sin exposición de stacktraces. |
| §2.5 Manejo de errores | Errores de schema se traducen en warnings de drf-spectacular, no en errores HTTP 500. |
| §3 Checklist Revisor/QA | En producción (`DEBUG=False`), los endpoints requieren `IsAdminUser`. No hay fuga de información. |

### 10.7. Cobertura de Endpoints

La integración documenta automáticamente todos los ViewSets registrados y endpoints funcionales:

| Tipo | Cantidad | Detalle |
|------|:--------:|---------|
| ViewSets CRUD | 27 | personas (7), salud (5), eventos (2), obra_social (2), talleres (11) |
| @action endpoints | 4 | `personaep` en Diagnostico, Evolucion, OS, Indicacion |
| Endpoints funcionales | 6 | login, create_user, users, update_user, refresh_token, health |
| **Total endpoints** | **37** | 33 rutas base + 4 @action |

### 10.8. Verificación

```bash
# 1. Verificar integridad del proyecto
python manage.py check                    # → 0 errores

# 2. Generar schema para validación
python manage.py spectacular --file schema.yaml   # → archivo YAML sin errores

# 3. Verificar que endpoints existentes siguen funcionando
curl -s http://localhost:8081/api/health          # → {"status": "ok", ...}
```

### 10.9. Exclusiones de este anexo

- ✗ No se modifican modelos, vistas, serializadores o servicios existentes
- ✗ No se genera documentación para endpoints que no estén bajo `/api/`
- ✗ No se implementa autenticación OAuth2 en Swagger UI (solo JWT Bearer)
- ✗ No se agregan tests unitarios para la documentación
- ✗ No se migra a SIDECAR para assets locales (queda como mejora futura)

---

## Aprobación del Anexo

| Rol | Estado | Fecha |
|-----|--------|-------|
| **Arquitecto** (emisor) | ✅ FIRMADO | 2026-07-04 |
| **Gatekeeper (DISEÑO)** | ⏳ Pendiente | 2026-07-04 |
| **Aprobación humana** | ⏳ Pendiente | 2026-07-04 |
