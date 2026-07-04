# REQUERIMIENTOS — CICLO CICLO-20260703-002

## Modo
`BROWNFIELD`

## Contexto
El proyecto Telepark es actualmente una aplicación Django monolítica: todo el dominio (26 modelos, 15 servicios, 16 ViewSets, 19 serializadores) vive dentro de una única app `teleparkApi`. Aunque en el ciclo anterior se extrajo una capa de servicios (`services.py`), el código sigue siendo un monolito en un solo módulo Python — alto acoplamiento, baja cohesión, y sin fronteras explícitas entre contextos del dominio.

**Hallazgo M001 (BASELINE.md):** Monolito — 26 modelos + 16 ViewSets + 15 servicios en un solo módulo.

Este ciclo busca dividir el monolito en **contextos delimitados (Bounded Contexts)** cohesivos e independientes, siguiendo los principios de Domain-Driven Design (DDD) táctico. Cada contexto será un módulo Django autocontenido con sus propios modelos, servicios, serializadores, vistas y URLs.

---

## User Stories

| ID | Rol | Quiero | Para |
|----|-----|--------|------|
| US-01 | Arquitecto | Que el dominio `personas` (Persona, PersonaEp, Direccion, Localidad, Municipio, Tipoparentesco) sea un módulo autocontenido con sus modelos, servicios, serializadores y vistas | Que sea el contexto raíz del que dependan los demás módulos sin acoplamiento directo |
| US-02 | Arquitecto | Que el dominio `obra_social` (Obrasocial, Os) sea un módulo independiente para la gestión de coberturas médicas | Aislar la lógica de obra social del núcleo clínico |
| US-03 | Arquitecto | Que el dominio `eventos` (Evento, TipoEvento) sea un módulo independiente para la gestión de eventos y tipos de evento | Separar la trazabilidad de eventos (altas, bajas, cambios) del resto del sistema |
| US-04 | Arquitecto | Que el dominio `talleres` (Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo, Valorvariableuo) sea un módulo independiente | Separar el módulo de talleres terapéuticos del núcleo de pacientes |
| US-05 | Arquitecto | Que el dominio `salud` (Diagnostico, Evolucion, Enfermedad, Medicamento, Indicacionmedicamento) sea un módulo unificado que agrupe lo clínico y lo farmacéutico | Tener un contexto cohesivo de salud del paciente sin dividir artificialmente diagnóstico de prescripción |
| US-06 | Arquitecto | Que el módulo `core` contenga la infraestructura compartida (authentication, middleware, helpers, permission, static) | Mantener la lógica transversal en un lugar único y reutilizable |
| US-07 | Arquitecto | Que no existan dependencias circulares entre los módulos resultantes | Mantener un grafo de dependencias acíclico que sea mantenible y testeable |
| US-08 | QA Engineer | Poder verificar que todos los endpoints existentes funcionan idénticamente tras la división en módulos (sin regresiones) | Asegurar que la reestructuración es puramente arquitectónica y no introduce cambios funcionales |

---

## Criterios de Aceptación (EARS)

### Ubiquitous (comportamiento siempre activo)

| ID | Criterio |
|----|----------|
| REQ-01 | El sistema DEBE tener un módulo `personas/` (Django app) con sus propios `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py` y `migrations/` |
| REQ-02 | El módulo `personas/` DEBE contener los modelos Persona, PersonaEp, Direccion, Localidad, Municipio y Tipoparentesco |
| REQ-03 | El sistema DEBE tener un módulo `obra_social/` con sus propios `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py` y `migrations/` |
| REQ-04 | El módulo `obra_social/` DEBE contener los modelos Obrasocial y Os |
| REQ-05 | El sistema DEBE tener un módulo `eventos/` con sus propios `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py` y `migrations/` |
| REQ-06 | El módulo `eventos/` DEBE contener los modelos Evento y Tipoevento |
| REQ-07 | El sistema DEBE tener un módulo `talleres/` con sus propios `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py` y `migrations/` |
| REQ-08 | El módulo `talleres/` DEBE contener los modelos Taller, Clasetaller, Actividad, Actividadrealizada, Asistenciataller, Comportamiento, Factorclase, Factorglobal, Unidadobservacion, Variableuo y Valorvariableuo |
| REQ-09 | El sistema DEBE tener un módulo `salud/` con sus propios `models.py`, `services.py`, `serializers.py`, `views.py`, `urls.py` y `migrations/` |
| REQ-10 | El módulo `salud/` DEBE contener los modelos Diagnostico, Evolucion, Enfermedad, Medicamento e Indicacionmedicamento |
| REQ-11 | El sistema DEBE tener un módulo `core/` con la infraestructura compartida: authentication, middleware, helpers, permission, static, y el health_check |
| REQ-12 | El grafo de dependencias entre módulos DEBE ser acíclico (DAG) — ningún módulo puede importar directa o transitivamente desde un módulo que dependa de él |
| REQ-13 | El módulo `personas/` NO DEBE tener dependencias de ningún otro módulo de dominio (es el contexto base raíz) |
| REQ-14 | `python manage.py check` DEBE reportar 0 errores tras la reestructuración |

### Event-driven (respuesta a eventos)

| ID | Criterio |
|----|----------|
| REQ-15 | CUANDO un modelo en un módulo A referencie mediante FK a un modelo del módulo `personas/`, DEBE usar la sintaxis `'personas.NombreModelo'` (string-based FK), NO importando directamente la clase del modelo |
| REQ-16 | CUANDO se ejecute `python manage.py test` tras la migración, el sistema DEBE pasar todas las pruebas existentes sin errores de importación |
| REQ-17 | CUANDO un módulo dependa de otro (ej: salud → personas), DEBE declarar esa dependencia explícitamente en su `apps.py` mediante `name` de Django app |

### State-driven (comportamiento condicional)

| ID | Criterio |
|----|----------|
| REQ-18 | MIENTRAS los modelos estén distribuidos en módulos separados, las rutas de API DEBEN mantener el mismo prefijo `/api/` que tenía el monolito (no se cambian URLs) |
| REQ-19 | MIENTRAS un serializer serialice modelos de otro módulo (ej: un serializer de `salud` serializa un modelo de `personas`), DEBE importar el serializer del módulo origen de manera explícita |

### Unwanted-behavior (manejo de errores)

| ID | Criterio |
|----|----------|
| REQ-20 | SI durante la división en módulos se rompe algún endpoint existente, ENTONCES el ciclo DEBE rechazarse y reportar el error específico |
| REQ-21 | SI dos módulos quedan con dependencia circular, ENTONCES el diseño DEBE rechazarse y el Arquitecto DEBE proponer una topología alternativa |

### Optional-feature (características opcionales)

| ID | Criterio |
|----|----------|
| REQ-22 | DONDE se detecten servicios faltantes (ej: modelos Taller sin servicios), el Arquitecto PUEDE proponer la creación de servicios básicos como parte del diseño |
| REQ-23 | DONDE sea necesario, el Arquitecto PUEDE proponer un archivo `urls.py` central en `core/` que agregue las rutas de todos los módulos |

---

## Trazabilidad US ↔ REQ

| User Story | Criterios EARS |
|------------|----------------|
| US-01 — Módulo personas | REQ-01, REQ-02, REQ-13 |
| US-02 — Módulo obra_social | REQ-03, REQ-04, REQ-15, REQ-17 |
| US-03 — Módulo eventos | REQ-05, REQ-06, REQ-15, REQ-17 |
| US-04 — Módulo talleres | REQ-07, REQ-08, REQ-15, REQ-17 |
| US-05 — Módulo salud | REQ-09, REQ-10, REQ-15, REQ-17 |
| US-06 — Módulo core | REQ-11 |
| US-07 — Sin ciclos | REQ-12, REQ-21 |
| US-08 — Sin regresiones | REQ-14, REQ-16, REQ-18, REQ-20 |

---

## Trazabilidad REQ ↔ Hallazgos BASELINE.md

| Criterio EARS | Hallazgo asociado |
|---------------|-------------------|
| REQ-01 a REQ-11 | **M001** — Monolito en teleparkApi |
| REQ-12, REQ-21 | **M001** — Sin dependencias circulares |
| REQ-22 | **M002** — Sin servicios para Talleres |
| REQ-23 | **M003** — Serializadores con acoplamiento cruzado |
| REQ-11 | **M004** — Archivos planos transversales |

---

## Topología de Módulos (consensuada)

```
                    ┌──────────────────────────┐
                    │   core (shared kernel)    │
                    │  authentication. helpers  │
                    │  middleware, permission,  │
                    │  static, health_check     │
                    │  (NO tiene modelos)       │
                    └──────────────────────────┘

                    ┌──────────────────────────┐
                    │      personas             │
                    │  (CONTEXTO RAÍZ)          │
                    │  Persona, PersonaEp       │
                    │  Direccion, Localidad     │
                    │  Municipio, Tipoparentesco│
                    └──────┬────────────────┬───┘
                           │                │
              ┌────────────▼──┐    ┌────────▼───────────┐
              │    salud      │    │     talleres        │
              │  Diagnostico  │    │  Taller, Clasetaller│
              │  Evolucion    │    │  Actividad, Act.    │
              │  Enfermedad   │    │  Asistenciataller   │
              │  Medicamento  │    │  Comportamiento     │
              │  Indicacion   │    │  Factor*, Variable* │
              └──────┬────────┘    └─────────────────────┘
                     │
                     └──────────┬────────────┐
                                ▼            ▼
                        ┌────────────┐ ┌────────────┐
                        │ eventos    │ │ obra_social│
                        │ Evento     │ │ Obrasocial │
                        │ TipoEvento │ │ Os         │
                        └────────────┘ └────────────┘
```

**Grafo de dependencias (DAG):**

```
personas ──→ (ninguno)            ← contexto raíz
core     ──→ (ninguno)            ← plano, no tiene modelos
salud    ──→ personas             ← Diagnostico, Evolucion, Indicacion → PersonaEp
eventos  ──→ personas             ← Evento → PersonaEp
obra_social ──→ personas          ← Os → PersonaEp
talleres ──→ personas             ← Asistenciataller → PersonaEp
```

**✅ Cero dependencias circulares — DAG puro.**

---

## Fuera de Alcance

| Item | Justificación |
|------|---------------|
| Migrar de MySQL a otra base de datos | No aplica a la reestructuración arquitectónica |
| Refactorizar authentication.py (A003, B004) | Pendiente de ciclo futuro de seguridad |
| Agregar tests unitarios nuevos | Este ciclo es puramente arquitectónico/estructural |
| Implementar event bus o mensajería entre contextos | Los contextos comparten BD (misma base MySQL) |
| Cambiar lógica de negocio existente | Solo se mueven archivos, no se modifica comportamiento |
| Renombrar modelos o modificar campos | Solo se redistribuye el código existente |
| Dockerizar los módulos por separado | Los módulos son lógicos dentro del mismo proceso Django |

---

## Notas Técnicas

- **Estructura objetivo:**
  ```
  telepark-backend/
  ├── telepark/                    (proyecto — configuración)
  │   ├── settings.py              (INSTALLED_APPS actualizado)
  │   └── urls.py                  (apunta a core.urls)
  ├── core/                        (infraestructura compartida)
  │   ├── apps.py
  │   ├── authentication.py
  │   ├── middleware.py
  │   ├── helpers.py
  │   ├── permission.py
  │   ├── static.py
  │   ├── urls.py                  (router central que agrega rutas de todos los módulos)
  │   └── views.py                 (health_check)
  ├── personas/
  │   ├── apps.py
  │   ├── models.py
  │   ├── services.py
  │   ├── serializers.py
  │   ├── views.py
  │   ├── urls.py
  │   └── migrations/
  ├── salud/
  ├── eventos/
  ├── obra_social/
  ├── talleres/
  └── manage.py
  ```

- **Referencias FK entre módulos:** Usar sintaxis `'personas.PersonaEp'` en el `ForeignKey` para evitar acoplamientos circulares en tiempo de importación.
- **Migraciones:** Se regenerarán desde cero para reflejar la nueva topología de módulos.
- **settings.py:** Se agregarán a `INSTALLED_APPS` los 6 nuevos módulos. Se eliminará `teleparkApi`.
- **URLs:** `core/urls.py` actuará como router central, importando las rutas de cada módulo.
