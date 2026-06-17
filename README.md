# Organización FEM - Portal Institucional

Este repositorio contiene la base completa del proyecto web institucional para **Organización FEM**, desarrollado con Python, FastAPI, plantillas Jinja2 y Sass para la gestión de estilos visuales.

---

## Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu entorno local:
- **Python 3.9 o superior**
- **Node.js (v18+)** y **npm** (para la compilación de estilos CSS/Sass)

---

## Guía de Instalación y Ejecución

### 1. Clonar e Instalar Dependencias de Python
En tu terminal, clona el proyecto y crea un entorno virtual de Python:

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar el entorno virtual (macOS / Linux)
source venv/bin/activate

# Activar el entorno virtual (Windows)
# venv\Scripts\activate

# Instalar dependencias requeridas
pip install -r requirements.txt
```

### 2. Instalar Dependencias de Estilos y Compilar SCSS
Usamos Dart Sass a nivel local para transpilar estilos SCSS ubicados en `app/static/src/scss/` a CSS estático consumido por las plantillas:

```bash
# Instalar dependencias (Sass compiler)
npm install

# Compilar los estilos por única vez
npm run build:css
```

> **Consejo durante desarrollo:** Para que los estilos se compilen de forma automática cada vez que guardas un cambio en los archivos `.scss`, mantén corriendo este comando en una terminal abierta secundaria:
> ```bash
> npm run watch:css
> ```

### 3. Ejecutar el Servidor Local
Con el entorno virtual activo y los estilos compilados, ejecuta el servidor local de desarrollo usando Uvicorn:

```bash
uvicorn app.main:app --reload
```

El servidor web estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Ejecución de Pruebas Unitarias
El proyecto cuenta con una batería básica de pruebas mediante Pytest para asegurar que el servidor responde adecuadamente en sus páginas principales:

```bash
pytest
```

---

## Documentación del Proyecto
Para más detalles sobre las directrices de desarrollo, consulta la carpeta `/docs`:
- **[Arquitectura General del Proyecto](organizacion-fem/docs/architecture.md)**
- **[Guía de Onboarding y Reglas para Gianluca](organizacion-fem/docs/onboarding.md)**