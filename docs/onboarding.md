# Onboarding para Gianluca - Guía de Desarrollo

¡Hola Gianluca! Bienvenido al equipo de desarrollo de **Organización FEM**.

Este documento te ayudará a dar tus primeros pasos en el proyecto, entender cómo trabajamos en equipo y conocer las reglas de desarrollo y fronteras del código para que puedas avanzar con total confianza sin romper la aplicación.

---

## 1. Zonas de Trabajo (Seguras vs Protegidas)

Para organizar las tareas y darte autonomía, hemos dividido el proyecto en dos áreas principales:

### 🟢 Zonas Seguras (Podés trabajar con libertad)
* **`app/templates/`**: Creación y edición de páginas HTML, parciales y layouts. Podés crear nuevos componentes en `components/macros.html` o estructurar nuevas vistas institucionales (ej. nuevas secciones informativas).
* **`app/static/src/scss/`**: Creación de estilos Sass. Podés modificar colores, márgenes y diseñar componentes gráficos en `_components.scss` o `_layout.scss`.
* **`app/routers/public.py`**: Agregar nuevas páginas públicas (ej. `/contacto`, `/servicios`).

### 🔴 Zonas Protegidas (Requieren revisión previa / No editar directamente)
* **`app/main.py`**: Configuración principal de FastAPI, inicialización de dependencias y middlewares. Si necesitás montar un nuevo middleware o agregar integraciones globales, consultalo antes de hacer commits.
* **`app/core/templates.py`**: Configuración del motor de Jinja2. Modificarlo podría romper la resolución de rutas de todo el sitio.
* **`app/routers/admin.py`**: Rutas de administración interna y futuros esquemas de autenticación.
* **`requirements.txt` y `package.json`**: Versiones de librerías Python y npm. Si necesitás agregar un paquete nuevo, creá una tarea de discusión primero.

---

## 2. Reglas de Código Obligatorias

### A. Firma de Respuesta de Plantillas (Jinja2)
Debido a particularidades de compatibilidad en FastAPI/Starlette, **todas** las rutas que renderizan plantillas HTML deben inyectar el objeto `request` de tipo `Request` y pasarlo obligatoriamente en `TemplateResponse`.

**Ejemplo correcto (Seguir siempre este patrón):**
```python
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("/mi-nueva-pagina", response_class=HTMLResponse)
async def nueva_pagina(request: Request):
    return templates.TemplateResponse(
        request=request,               # <-- OBLIGATORIO: Pasa el request de forma explicita
        name="mi_plantilla.html",
        context={"mi_variable": "Hola Gianluca"}
    )
```

### B. Compilación de Estilos SCSS
Nunca escribas estilos directamente en el archivo compilado `app/static/dist/css/main.css`, ya que este se sobrescribe automáticamente en cada compilación.

- Escribí tus estilos dentro de la carpeta `app/static/src/scss/`.
- Mientras programás, corré el comando de observación en una terminal aparte para ver tus cambios reflejados al instante:
  ```bash
  npm run watch:css
  ```
- Si agregás un archivo SCSS nuevo (ej. `_forms.scss`), recordá importarlo en la cabecera del archivo principal `app/static/src/scss/main.scss`:
  ```scss
  @import "variables";
  @import "base";
  @import "layout";
  @import "components";
  @import "forms"; // <-- Tu nueva hoja de estilos
  ```

---

## 3. Flujo de Trabajo Colaborativo (Git y Testing)

1. **Creación de ramas:** Para cada tarea, creá una rama con un nombre claro basado en la convención:
   `git checkout -b feature/gianluca/nombre-de-la-tarea`
2. **Desarrollo Local:** Hacé tus cambios respetando las zonas seguras.
3. **Pruebas Locales:** Antes de hacer commit y subir tus cambios, asegurate de correr los tests automatizados para validar que las rutas sigan respondiendo correctamente:
   ```bash
   pytest
   ```
4. **Pull Request (PR):** Sube tus cambios a GitHub y abrí un Pull Request hacia la rama `main` o `develop`. Asigná a otro desarrollador como revisor para aprobar y mergear la tarea.
