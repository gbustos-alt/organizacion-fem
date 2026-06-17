# Arquitectura del Proyecto - Organización FEM

Este documento describe la arquitectura técnica, la estructura de directorios y el flujo de ejecución de la plataforma web de Organización FEM.

---

## 1. Estructura del Proyecto

El proyecto está diseñado como un paquete Python modular bajo la carpeta `app/`, junto con herramientas para el flujo de trabajo colaborativo y de activos en la raíz:

```text
organizacion-fem/
├── app/
│   ├── __init__.py          # Inicialización del paquete app
│   ├── main.py              # Bootstrap de FastAPI, static files, routers y manejadores de errores
│   ├── core/
│   │   └── templates.py     # Instanciación global de Jinja2Templates (evita importaciones circulares)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── public.py        # Rutas institucionales públicas (Home, Nosotros, etc.)
│   │   └── admin.py         # Rutas de administración interna (Módulo Admin / Panel)
│   ├── templates/           # Vistas Jinja2 (HTML5 semántico)
│   │   ├── base.html        # Plantilla maestra principal
│   │   ├── index.html       # Landing page institucional
│   │   ├── nosotros.html    # Sección de información Quiénes Somos
│   │   ├── admin_dashboard.html # Panel administrativo placeholder
│   │   ├── 404.html         # Página de error recurso no encontrado
│   │   ├── 500.html         # Página de error interno
│   │   ├── components/      # Componentes Jinja2 reutilizables
│   │   │   └── macros.html  # Macros helper (render_button, render_card, etc.)
│   │   └── partials/        # Partes fijas reutilizadas mediante include
│   │       ├── header.html
│   │       └── footer.html
│   └── static/              # Archivos estáticos servidos por FastAPI
│       ├── dist/
│       │   └── css/         # Hojas de estilo compiladas finales (main.css)
│       ├── src/
│       │   └── scss/        # Hojas de estilo en desarrollo (Sass)
│       │       ├── main.scss
│       │       ├── _variables.scss
│       │       ├── _base.scss
│       │       ├── _layout.scss
│       │       └── _components.scss
│       └── js/
│           └── main.js      # Interactividad cliente general
├── docs/                    # Documentación de arquitectura y onboarding
│   ├── architecture.md
│   └── onboarding-junior.md
├── tests/                   # Pruebas automatizadas (Pytest)
│   └── test_main.py
├── package.json             # Herramientas Sass npm (Frontend assets)
├── requirements.txt         # Dependencias Python
└── README.md                # Guía rápida de inicialización
```

---

## 2. Flujo de Enrutamiento y Controladores

Utilizamos `APIRouter` de FastAPI para modularizar las secciones de la aplicación y mantener el código ordenado a medida que el proyecto crece:

- **Router Público (`app/routers/public.py`):** Encargado de las rutas institucionales abiertas. Todas las rutas que renderizan plantillas HTML de Jinja2 **deben** inyectar el parámetro `request: Request` y pasarlo en el llamado `templates.TemplateResponse`.
- **Router Administrativo (`app/routers/admin.py`):** Contiene el punto de entrada al panel de gestión interno bajo el prefijo `/admin`. En esta etapa inicial actúa como un placeholder limpio donde posteriormente se agregará autenticación y validación de sesiones.

---

## 3. Sistema de Plantillas (Jinja2)

La renderización se maneja usando la integración nativa de Jinja2 en FastAPI:

- **Herencia de Plantillas:** La plantilla base `base.html` provee el esqueleto general (HTML5, metas SEO, CSS final y JS básico) y define bloques (`{% block content %}`, `{% block title %}`) que son extendidos por las páginas individuales (`index.html`, `nosotros.html`).
- **Macros y Componentes:** Definidos en `templates/components/macros.html`. Permiten encapsular HTML repetitivo (como botones institucionales o tarjetas informativas) con parámetros reutilizables.
- **Evitar Errores de Starlette:** Se ha configurado el módulo `app/core/templates.py` de forma separada del archivo principal `main.py`. Esto previene la importación circular entre los routers que necesitan renderizar vistas y el código principal de configuración de la app.

---

## 4. Pipeline de Hojas de Estilos (SCSS a CSS)

El diseño del sitio web se gestiona a través de Sass (SCSS) ubicado en `app/static/src/scss/`:

1. **Variables y Tokens:** Todo el sistema visual (colores, fuentes, sombras) se define como variables CSS en el elemento `:root` dentro de `_variables.scss`. Esto asegura que las Custom Properties de CSS sean la única fuente de verdad y permite adaptar el tema fácilmente en el navegador.
2. **Modularización:** La hoja de estilo principal `main.scss` importa de forma ordenada los archivos parciales de variables, bases y componentes utilizando `@import`.
3. **Compilación:** Un script local de Node (configurado en `package.json` utilizando la librería Dart Sass) compila los archivos `.scss` directamente al archivo estático optimizado `app/static/dist/css/main.css`.
