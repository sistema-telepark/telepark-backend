# CONSTITUCIÓN DEL SISTEMA Y ESTÁNDARES GLOBALES (GLOBAL RULES)
> **ESTADO:** INMUTABLE. 
> **DIRECTIVA PARA AGENTES:** Ningún agente tiene permiso para modificar este archivo. Estas reglas tienen precedencia absoluta sobre cualquier decisión técnica.

## 1. Arquitectura de Capas (Flujo de Dependencia Unidireccional)
El sistema DEBE estructurarse estrictamente en tres capas:
- **Capa de Presentación (Views/Serializers):** Responsable única de HTTP. PROHIBIDO contener lógica de negocio.
- **Capa de Lógica de Negocio (Services):** Encapsula reglas de negocio. PUEDE importar Modelos y ORM.
- **Capa de Acceso a Datos (Models/Managers):** Representada por el ORM de Django.

---

## 2. Estándares de Seguridad (OWASP & Security by Design)
**Referencia Base:** OWASP Top 10 (Web & API Security).
**Alcance:** Obligatorio para todas las capas.

### 2.1. Límites de Confianza
- **Aislamiento del Dominio:** Las entidades core jamás deben recibir objetos HTTP crudos. Todo dato debe estar validado por adaptadores de entrada.

### 2.2. Validación de Entradas (White-listing)
- **Tipado Fuerte:** Usar validación de esquemas (Pydantic/Serializers) forzando tipos y formatos.
- **White-listing:** Validar contra lo permitido, nunca buscar lo prohibido.
- **Inyección:** PROHIBIDA la concatenación de strings para queries. Uso obligatorio del ORM de Django.

### 2.3. Identidades y Control de Acceso (IAM)
- **Autenticación:** Uso de tokens seguros (JWT/OAuth2) con TTL corto.
- **Autorización:** Verificación a nivel de endpoint y recurso (prevención de IDOR/BOLA).
- **Gestión de Secretos:** PROHIBIDO hardcodear. Uso obligatorio de variables de entorno.

### 2.4. Protección de Datos y Criptografía
- **Datos en Tránsito:** TLS 1.2 o superior.
- **Datos en Reposo:** Hasheo robusto (Argon2/bcrypt) para contraseñas; cifrado de PII a nivel de base de datos.
- **Cabeceras:** Configurar CORS, HSTS, X-Content-Type-Options.

### 2.5. Observabilidad y Logging
- **Sanitización:** Los logs NUNCA deben imprimir datos sensibles (PII, tokens, credenciales).
- **Manejo de Errores:** No exponer Stacktraces al cliente. Respuestas genéricas RFC 7807.

---

## 3. Checklist de Auditoría (Para Revisor y QA)
El Revisor y el QA DEBEN rechazar cualquier flujo que infrinja:
- [ ] Endpoints sin autenticación/autorización explícita.
- [ ] Lógica de negocio dentro de `Views`.
- [ ] Variables de entorno no validadas al arranque.
- [ ] Falta de *negative testing* (payloads maliciosos, roles sin permisos).
- [ ] Uso de queries directas sin parametrizar.