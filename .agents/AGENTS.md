# Estándar de Ingeniería Empresarial y Desarrollo de Alta Gama (Enterprise Quality Standard)

Este documento rige todos los desarrollos de software, refactorizaciones, diseños UI/UX y despliegues realizados en este proyecto.

---

## 1. Arquitectura & Limpieza de Código (Enterprise Backend)
- **Separación de Responsabilidades (SOLID)**: 
  - La lógica de negocio reside exclusivamente en la capa de servicios (`services/`).
  - Los routers/controladores (`routers/`) son delgados y solo gestionan transporte HTTP, validación y respuestas DTO.
  - La persistencia de datos reside en modelos declarativos (`models/`).
- **Seguridad & RBAC por Diseño**:
  - Todo endpoint o vista protegida debe verificar permisos RBAC antes de ejecutar lógica de negocio.
  - Toda mutación de datos debe registrar un evento de auditoría en la base de datos (`AuditoriaEvento`).
  - Sanitización y validación estricta de entrada vía esquemas Pydantic / DTOs.
- **Causa Raíz Profunda (Zero Symptom Patching)**:
  - Prohibido enmascarar errores capturando excepciones de forma silenciosa, retornando valores fallback vacíos o suprimiendo fallos de tests. Todo error debe rastrearse aguas arriba hasta su causa raíz.

---

## 2. Frontend de Alta Gama & UX Responsivo (Enterprise Frontend)
- **Sistema de Tokens Centralizado**:
  - Todos los colores, espaciados, sombras y fuentes provienen del sistema de tokens (`tokens.scss` o variables CSS). Prohibido hardcodear offsets arbitrarios o estilos ad-hoc.
- **Accesibilidad & Touch Target (WCAG AA)**:
  - Todo elemento interactivo móvil debe tener un área de contacto mínima de **44x44px**.
  - Todo texto e ícono debe cumplir con un ratio de contraste mínimo de **4.5:1** (WCAG AA).
- **Animaciones Serenas a 60 FPS (Cero Despliegues Bruscos)**:
  - Prohibido animar directamente entre `display: none` y `display: block`.
  - Los desplegables y acordeones deben utilizar animación por cuadrícula CSS (`grid-template-rows: 0fr -> 1fr`) o `opacity` + `transform` para garantizar 60 fps sin saltos verticales.
- **Scoping Estricto de Media Queries**:
  - Estilos, transformaciones y hover de escritorio deben estar estrictamente encapsulados dentro de `@media (min-width: 768px)`. Prohibido contaminar eventos táctiles móviles.
- **Cache-Busting Automático**:
  - Al modificar cualquier asset estático (CSS, JS, imágenes), se debe incrementar obligatoriamente la versión de la consulta `?v=N` en los templates para evitar cachés residuales de navegador o CDN.

---

## 3. Protocolo de Verificación & Despliegue Definitivo (CI/CD & Deploy)
- **Verificación Local Obligatoria**:
  - Antes de declarar un trabajo como finalizado o realizar un commit, el agente DEBE:
    1. Recompilar los assets de producción (`npm run build:css` / `build`).
    2. Ejecutar la suite completa de pruebas unitarias/integración (`pytest` / `npm test`) asegurando 100% de pasaje.
- **Despliegue Atómico y Limpio**:
  - Todo script de despliegue (`deploy.sh` o pipeline) debe ejecutar la secuencia atómica:
    1. Descarga de código (`git pull`).
    2. Migración de base de datos / compilación de assets si aplica.
    3. Reinicio automático del servicio (`systemctl` / `pm2` / `docker`).
    4. Invalidation de caché HTTP.
    5. Retorno limpio de exit code 0.

---

## 4. Modo Mentor & Comunicación
- Explicar brevemente la fundamentación técnica detrás de cada patrón elegido, las alternativas evaluadas y la razón por la cual la solución previene deuda técnica a largo plazo.
- Cero respuestas aduladoras; enfoque directo al trabajo y evidencia empírica de funcionamiento.
