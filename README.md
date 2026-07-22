# Fundación Educación y Misión (FEM) — Portal Web e Infraestructura Digital

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![Sass](https://img.shields.io/badge/Sass-Dart_Sass-CC6699.svg?style=flat&logo=sass)](https://sass-lang.com/)
[![Tests](https://img.shields.io/badge/Tests-28%2F28_Passed-success.svg?style=flat&logo=pytest)](https://docs.pytest.org/)

El portal web institucional de la **Fundación Educación y Misión (FEM)** es una plataforma digital de alto impacto diseñada para el acompañamiento, conducción y resguardo carismático de comunidades educativas católicas en la República Argentina (promovida por FAERA).

La aplicación integra una **Home Narrativa Escénica basada en el patrón *Layered Reveal Foundation*** (5 capas inmersivas con fotografía full-bleed, cabecera adaptativa glassmorphism y transiciones editoriales serenas), un catálogo interactivo de la Red Federal de Colegios con cartografía dinámica en Leaflet.js, y un **Panel de Gestión Administrativo completo (RBAC)** con soporte para inteligencia artificial (`agente_service`).

---

## 🌟 Características Principales

### 1. Experiencia de Navegación Home (*Layered Reveal Foundation v10*)
- **5 Escenas Inmersivas**: Hero Lema 2026, Identidad Institucional, Dimensiones de Acompañamiento, Novedades / Comunidad y Cierre Institucional / Recursero.
- **Cabecera Adaptativa Glassmorphism**: Menú lineal transparente en estado reposo sobre fotografías inmersivas, con transición automática a *Azul Catedral Glass Blur* (`rgba(12, 30, 54, 0.82)`) y elevación por sombra al hacer scroll, garantizando contraste 100% perfecto sobre cualquier fondo.
- **Transiciones de Texto Serenas (*Fade-Dominant Motion*)**: Movimientos pausados con desvanecidos graduales (`opacity: 0 ↔ 1`), translaciones verticales sutiles (`10px–12px`) y ritmo escalonado (*staggered motion*) en titulares, párrafos y botones.
- **Resolución Mobile 100svh & Carro Escénico**: En móviles (`< 768px`), cada escena ocupa `100svh` con scroll-snap nativo y actualización dinámica de fondos según la tarjeta activa.
- **Indicador de Progreso Lateral (`lr-nav-progress`)**: Widget de navegación vertical con barra de llenado dinámico, puntos activos con tooltip e interacción fluida.

### 2. Portal Público Institucional
- **Misión y Visión**: Exposición de los ejes rectores, inspiraciones carismáticas y citas del Papa Francisco.
- **Identidad & Gobierno**: Estructura organizacional, órganos de gobierno y representatividad de FAERA.
- **Dimensiones de Acompañamiento**: Sección interactiva de las áreas Pedagógica, Administrativa, Legal y Pastoral.
- **Red Federal de Colegios**: Mapa interactivo cartográfico (Leaflet.js) con geolocalización de escuelas, filtros territoriales y fichas detalladas por establecimiento.
- **Recursero & Publicaciones**: Repositorio de materiales pedagógicos y documentos descargables.
- **Memorias de Gestión**: Histórico de balances y transparencia institucional.
- **Canales de Formulario**: Incorporación para nuevas comunidades educativas, carga de CV para educadores ("Trabaja con Nosotros") y consultas para Congregaciones.

### 3. Panel de Administración `/admin` (RBAC)
- **Autenticación Segura y Control de Acceso por Roles (RBAC)**: Roles de Administrador General, Gestor Institucional, Operador Pedagógico y Lector.
- **Gestión de Entidades**: Colegios, Alumnos, Novedades, Materiales/Publicaciones y Solicitudes de Incorporación.
- **Asistente de Inteligencia Artificial (`agente_service`)**: Integración con modelo conversacional para asistencia operativa y redacción institucional.
- **Sistema de Auditoría de Eventos**: Registro detallado de acciones en base de datos (`AuditoriaEvento`).

---

## 🛠️ Arquitectura y Tecnologías

```text
               +----------------------------------+
               |        Cliente (Browser)         |
               |  Jinja2 Render + SCSS + JS v10   |
               +----------------+-----------------+
                                | HTTP / JSON
                                v
               +----------------------------------+
               |          FastAPI App             |
               |  (routers/public & routers/admin)|
               +----------------+-----------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
+---------------+       +---------------+       +---------------+
| SQLAlchemy    |       | RBAC / Auth   |       | Agente IA     |
| SQLite ORM    |       | Service       |       | Service       |
+---------------+       +---------------+       +---------------+
```

- **Backend**: Python 3.9+, FastAPI, Uvicorn, SQLAlchemy ORM, Pydantic, Passlib (bcrypt), Pytest.
- **Frontend**: Plantillas Jinja2, Vanilla JavaScript ES6+ (modular), Leaflet.js (mapas).
- **Estilos**: Sass (Dart Sass), compilado a `frontend/css/main.css`.
- **Base de Datos**: Cloud SQLite / SQLite local (`fundacion_fem.db`).

---

## 📁 Estructura del Proyecto

```text
organizacion-fem/
├── backend/
│   ├── main.py                   # Punto de entrada de la aplicación FastAPI
│   ├── seed.py                   # Script de sembrado de datos iniciales
│   ├── core/
│   │   ├── database.py           # Configuración de Engine y Session SQLAlchemy
│   │   ├── templates.py          # Instancia de Jinja2Templates
│   │   └── role_seed.json        # Definición de roles y permisos RBAC
│   ├── models/                   # Modelos ORM (Auth, Colegio, Academico, Auditoria, etc.)
│   ├── routers/
│   │   ├── public.py             # Rutas públicas institucionales (Home, Identidad, Colegios, etc.)
│   │   └── admin/                # Rutas del Panel de Administración (12 módulos)
│   └── services/                 # Servicios de negocio (Auth, RBAC, Agente IA, Auditoría)
├── frontend/
│   ├── css/                      # CSS compilado y mapas de origen
│   ├── js/                       # Motor JS (layered-reveal.js, main.js, colegios.js)
│   ├── scss/                     # Código fuente SCSS (tokens, base, layout, components, pages)
│   │   └── components/
│   │       └── _layered_reveal.scss  # Motor visual Layered Reveal v10
│   └── templates/                # Plantillas Jinja2 (base, partials, home, admin)
├── docs/                         # Documentación técnica y guías de onboarding
├── tests/
│   └── test_main.py              # Suite de pruebas unitarias Pytest (28 tests)
├── notebook_context_fem.md       # Archivo compilado para exportar a Gemini Notebook
├── requirements.txt              # Dependencias de Python
├── package.json                  # Scripts de NPM (Dart Sass compiler)
└── README.md                     # Manual del repositorio
```

---

## 🚀 Guía de Instalación y Ejecución Local

### 1. Requisitos Previos
- **Python 3.9** o superior
- **Node.js (v18+)** y **npm**

### 2. Clonar e Instalar Dependencias de Python

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual en macOS / Linux
source venv/bin/activate

# Instalar dependencias de Python
pip install -r requirements.txt
```

### 3. Compilar Estilos SCSS (Dart Sass)

```bash
# Instalar paquete Sass de npm
npm install

# Compilar CSS para producción
npm run build:css

# Modo desarrollo (observador automático de cambios SCSS)
npm run watch:css
```

### 4. Sembrado Inicial de Datos (Opcional)

Para poblar la base de datos local con escuelas de prueba, usuarios por rol y contenidos:

```bash
PYTHONPATH=. python3 backend/seed.py
```

### 5. Iniciar Servidor de Desarrollo

```bash
uvicorn backend.main:app --reload
```

Accede al portal institucional en: **`http://127.0.0.1:8000`**  
Accede al panel de administración en: **`http://127.0.0.1:8000/admin/`**

---

## 🧪 Ejecución de Pruebas Unitarias

El proyecto incluye 28 pruebas automatizadas con Pytest que garantizan la integridad de todas las rutas públicas y del panel administrativo:

```bash
PYTHONPATH=. ./venv/bin/pytest
```

**Resultado:** `28 passed in 0.65s (100% OK)`

---

## 🗺️ Mapa de Rutas Principales

| Categoría | Método | Ruta | Descripción |
| :--- | :--- | :--- | :--- |
| **Público** | GET | `/` | Home Layered Reveal v10 (5 Escenas Inmersivas) |
| **Público** | GET | `/identidad` | Página de Identidad Institucional |
| **Público** | GET | `/mision` | Misión y Visión (Ejes Rectores) |
| **Público** | GET | `/organizacion` | Gobierno y Estructura Organizacional |
| **Público** | GET | `/dimensiones` | Dimensiones de Acompañamiento |
| **Público** | GET | `/colegios` | Red Federal de Colegios (Mapa Interactivo) |
| **Público** | GET | `/colegios/{id}` | Ficha Detallada de Establecimiento Educativo |
| **Público** | GET | `/materiales` | Repositorio de Material y Reflexión |
| **Público** | GET | `/memorias` | Memorias de Gestión y Balances |
| **Público** | GET | `/contacto` | Contacto Institucional |
| **Público** | POST| `/trabaja-con-nosotros` | Carga de CV para Educadores |
| **Público** | POST| `/congregaciones` | Solicitud de Acompañamiento Congregacional |
| **Admin** | GET | `/admin/` | Dashboard Administrativo |
| **Admin** | GET/POST| `/admin/auth/login` | Login y Autenticación de Usuarios |
| **Admin** | GET/POST| `/admin/colegios/` | ABM de Colegios de la Red |
| **Admin** | GET/POST| `/admin/alumnos/` | Gestión de Alumnos y Matrícula |
| **Admin** | GET/POST| `/admin/incorporaciones/` | Gestión de Solicitudes de Adhesión |
| **Admin** | GET/POST| `/admin/agente/` | Asistente Operativo con Inteligencia Artificial |

---

## 📚 Documentación Adicional

- **[Ficha para Gemini Notebook](notebook_context_fem.md)**: Archivo compilado listo para importar como fuente en Gemini Notebook / NotebookLM.
- **[Arquitectura General del Proyecto](docs/architecture.md)**
- **[Guía de Estándares Visuales](docs/guia_desarrollo_visual.md)**
- **[Propuesta Cromática](docs/propuesta-cromatica-clara.md)**
- **[Onboarding y Normas del Equipo](docs/onboarding.md)**

---

## ⚖️ Licencia y Propiedad

© 2026 Fundación Educación y Misión (FEM) | Todos los derechos reservados.  
Promovida por FAERA — Personería Jurídica Nacional.