# Cuaderno de Estudio y Contexto Técnico — Proyecto Organización FEM

> **Archivo de Exportación para Gemini Notebook / NotebookLM**  
> **Fecha de Compilación:** Julio 2026  
> **Proyecto:** Portal Web Institucional y Sistema de Gestión Administrativa para Fundación Educación y Misión (FEM)  
> **Framework:** FastAPI + Jinja2 + Dart Sass + Layered Reveal Engine v10 + SQLite SQLAlchemy

---

## 1. Visión General del Proyecto y Propósito Institucional

La **Fundación Educación y Misión (FEM)** es una fundación civil de bien público promovida por FAERA (Federación de Asociaciones Educativas Religiosas de la República Argentina) destinada al acompañamiento, conducción y resguardo carismático de comunidades educativas católicas en todo el territorio argentino.

El proyecto tecnológico abarca dos dimensiones integradas:
1. **Portal Web Institucional Público**: Diseñado con la narrativa escénica **Layered Reveal v10**, orientada a transmitir calidez, profesionalismo y sobriedad educativa sin caer en estetizaciones rígidas ni folletos tradicionales.
2. **Panel de Gestión Administrativa (`/admin`)**: Sistema integral con Control de Acceso Basado en Roles (RBAC), módulo de auditoría de eventos, gestión de matrículas, comunidades educativas, materiales pedagógicos y asistente de inteligencia artificial (`agente_service`).

---

## 2. Arquitectura Técnica de Software

### Stack Tecnológico Principal
- **Lenguaje Backend**: Python 3.9+
- **Framework Principal**: FastAPI (`fastapi.FastAPI`)
- **Servidor ASGI**: Uvicorn (`uvicorn`)
- **Motor de Plantillas**: Jinja2 (`jinja2.Environment`)
- **ORM / Base de Datos**: SQLAlchemy 2.0+ sobre SQLite (`fundacion_fem.db`)
- **Gestión de Estilos**: SCSS modular transpilado con Dart Sass (`npm run build:css`)
- **Motor de Animación Frontend**: JavaScript ES6+ Vanilla (Sin dependencias externas pesadas)
- **Mapas Interactivos**: Leaflet.js con marcadores CSS vectoriales personalizados
- **Suite de Pruebas**: Pytest + FastAPI `TestClient` (28 pruebas automatizadas)

---

## 3. Especificación Técnica del Motor Layered Reveal v10

El patrón **Layered Reveal** convierte la navegación de la página de inicio (Home) en una experiencia narrativa basada en 5 escenas inmersivas con fotografía de pantalla completa (*full-bleed*).

### Escenas Narrativas del Home (`frontend/templates/components/layered_reveal.html`):
1. **Escena 1 (Hero / Lema 2026)**: Fotografía principal de comunidad educativa, lema `#CaminandoJuntos`, título institucional y llamada a la acción principal.
2. **Escena 2 (Identidad)**: Tarjeta marco institucional con imagen curva de estudiantes y síntesis de la misión civil de resguardo carismático.
3. **Escena 3 (Dimensiones de Acompañamiento)**: Grilla fotográfica inmersiva de 4 tarjetas interactiva (Dimensiones Pedagógica, Administrativa, Legal y Pastoral).
4. **Escena 4 (Novedades & Comunidad)**: Galería de artículos y eventos institucionales en tarjetas vidriadas.
5. **Escena 5 (Recursero / Cierre Institucional)**: Cierre narrativo con enlaces a materiales curados y memorias de gestión.

### Innovaciones del Motor Visual v10:
- **Cabecera Adaptativa Glassmorphism**:
  - En estado reposo sobre la foto del Hero, el menú se presenta como una línea transparente vidriada ultraliviana (`rgba(86, 91, 98, 0.08)` con `backdrop-filter: blur(5px)`).
  - Al desplazarse en scroll sobre secciones con fondos claros o blancos, transiciona suavemente a **Azul Catedral Glass Blur (`rgba(12, 30, 54, 0.82)`)** con elevación por sombra inferior (`box-shadow: 0 10px 30px rgba(0, 0, 0, 0.38)`), garantizando contraste de lectura 100% perfecto (WCAG AAA) para las letras blancas.
- **Micro-animaciones Editoriales Serenas (*Fade-Dominant Motion*)**:
  - Opacidad suave (`opacity: 0 ↔ 1`) combinada con translaciones verticales sutiles de solo `10px–12px`.
  - Ritmo escalonado (*Staggered Rhythm*): Kicker (`0.05s`), Título (`0.12s`), Párrafo (`0.20s`), Acciones/Grillas (`0.28s`).
  - Curva de aceleración institucuonal `cubic-bezier(0.22, 1, 0.36, 1)`.
- **Adaptación Responsiva Móvil 100svh & Carro Escénico**:
  - En pantallas `< 768px`, cada escena toma `100svh` exactos.
  - Las grillas interiores se convierten automáticamente en un riel horizontal de 1 tarjeta por vista con scroll-snap y actualización dinámica del fondo.
- **Accesibilidad**: Respeto estricto por `prefers-reduced-motion` anulando translaciones físicas.

---

## 4. Diccionario de Datos y Modelo ORM (SQLAlchemy)

### Modelos Principales (`backend/models/`):

#### 1. Autenticación & Usuarios (`auth.py`)
- **`Usuario`**: `id`, `email`, `hashed_password`, `nombre_completo`, `rol_id`, `colegio_id`, `activo`, `created_at`.
- **`Rol`**: `id`, `nombre` (Admin, Gestor, Operador, Lector), `descripcion`, `permisos`.

#### 2. Colegios y Red Federal (`colegio.py`)
- **`Colegio`**: `id`, `nombre`, `cue`, `provincia`, `localidad`, `direccion`, `latitud`, `longitud`, `orientacion`, `imagen_url`, `historia`, `activo`.

#### 3. Académico y Matrícula (`academico.py`)
- **`Alumno`**: `id`, `colegio_id`, `nombre`, `apellido`, `dni`, `fecha_nacimiento`, `grado_año`, `tutor_nombre`, `tutor_contacto`, `activo`.
- **`Actividad`**: `id`, `colegio_id`, `titulo`, `descripcion`, `tipo` (Pastoral, Pedagógica, Comunidad), `fecha`.

#### 4. Solicitudes e Incorporación (`incorporacion.py`)
- **`SolicitudIncorporacion`**: `id`, `nombre_institucion`, `provincia`, `contacto_nombre`, `contacto_email`, `telefono`, `estado` (Pendiente, En Revisión, Aprobada, Rechazada), `created_at`.

#### 5. Auditoría de Seguridad (`auditoria.py`)
- **`AuditoriaEvento`**: `id`, `usuario_id`, `accion`, `entidad`, `detalles`, `ip_address`, `timestamp`.

---

## 5. Matriz de Seguridad y Roles (RBAC)

El archivo `backend/core/role_seed.json` y el servicio `backend/services/rbac_service.py` definen los niveles de autorización:

| Rol | Alcance de Permisos | Descripción |
| :--- | :--- | :--- |
| **Administrador General** | Full Access (`*:*`) | Control total sobre la plataforma, configuración, usuarios, colegios e IA. |
| **Gestor Institucional** | Lectura/Escritura en Colegios y Novedades | Administración operativa de escuelas asignadas y noticias. |
| **Operador Pedagógico** | Lectura/Escritura en Materiales y Alumnos | Carga de contenidos pedagógicos y seguimiento escolar. |
| **Lector** | Read-Only | Acceso a consulta en panel sin privilegios de modificación. |

---

## 6. Inventario de Endpoints (API & Vistas)

### Rutas Públicas (`backend/routers/public.py`):
- `GET /`: Home Layered Reveal v10 (5 Escenas Inmersivas).
- `GET /identidad`: Página de Identidad e Historia Institucional.
- `GET /mision`: Misión y Visión (Ejes Rectores y Citas del Papa Francisco).
- `GET /organizacion`: Gobierno, Consejo Superior y Estructura.
- `GET /dimensiones`: Áreas de Acompañamiento (Pedagógica, Administrativa, Legal, Pastoral).
- `GET /colegios`: Red Federal de Colegios (Mapa interactivo con Leaflet.js).
- `GET /colegios/{id}`: Ficha individual detallada de escuela.
- `GET /materiales`: Repositorio de Material y Reflexión Curada.
- `GET /memorias`: Memorias de Gestión y Transparencia.
- `GET /contacto`: Formulario e Información de Contacto Institucional.
- `POST /trabaja-con-nosotros`: Recepción de CV para educadores.
- `POST /congregaciones`: Solicitud de acompañamiento fraterno para Congregaciones.

### Rutas del Panel de Administración (`backend/routers/admin/`):
- `GET/POST /admin/auth/login`: Autenticación de usuarios por contraseña.
- `GET /admin/dashboard`: Métricas de control e impacto institucional.
- `GET/POST/PUT/DELETE /admin/colegios/`: ABM de la Red Federal de Colegios.
- `GET/POST/PUT/DELETE /admin/alumnos/`: Gestión de alumnos y matrícula.
- `GET/POST/PUT/DELETE /admin/novedades/`: Publicación de noticias y eventos.
- `GET/POST/PUT/DELETE /admin/materiales/`: Gestión del recursero pedagógico.
- `GET/POST/PUT/DELETE /admin/incorporaciones/`: Tratamiento de solicitudes de adhesión.
- `GET/POST /admin/agente/`: Asistente virtual impulsado por IA para tareas de gestión.
- `GET/POST/PUT/DELETE /admin/configuraciones/`: Parámetros globales del sistema.

---

## 7. Glosario Institucional FEM

- **FEM**: Fundación Educación y Misión. Fundación civil de bien público destinada al resguardo carismático de colegios católicos.
- **FAERA**: Federación de Asociaciones Educativas Religiosas de la República Argentina (Entidad promotora de la FEM).
- **Caminando Juntos**: Lema institucional que orienta la acción comunitaria.
- **Resguardo Carismático**: Acompañamiento legal, patrimonial, directivo y pastoral para asegurar la continuidad de escuelas cuya congregación fundadora no puede continuar la gestión directa.
- **Red Federal**: Conjunto de escuelas asociadas y acompañadas por FEM en distintas provincias argentinas.

---

## 8. Preguntas Frecuentes para Consultas en Gemini Notebook

1. **¿Qué tecnología utiliza el motor visual del Home y cómo se garantiza la legibilidad del menú sobre fondos blancos?**  
   *Respuesta:* Utiliza el motor Layered Reveal v10 (FastAPI + Jinja2 + SCSS + JS Vanilla). La legibilidad se garantiza mediante la cabecera adaptativa glassmorphism que en scroll se oscurece automáticamente a Azul Catedral (`rgba(12, 30, 54, 0.82)`) con desenfoque `blur(18px)`, otorgando contraste WCAG AAA a las letras blancas.

2. **¿Cómo se ejecutan las pruebas unitarias del proyecto?**  
   *Respuesta:* Se ejecutan con Pytest ejecutando `PYTHONPATH=. ./venv/bin/pytest`. La suite cuenta con 28 pruebas que verifican el 100% de la disponibilidad del portal público y admin.

3. **¿Cómo se compilan los estilos del proyecto?**  
   *Respuesta:* Se compilan desde la raíz del proyecto ejecutando `npm run build:css`, lo que invoca a Dart Sass para transpilar `frontend/scss/main.scss` hacia `frontend/css/main.css`.
