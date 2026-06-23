from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from backend.routers import public, admin
from backend.core.templates import templates
from backend.core.database import Base, engine
from backend import models  # Asegura el registro de todos los modelos en Metadata

# Crear tablas en base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Organización FEM",
    description="Portal institucional y administrativo de Organización FEM",
    version="1.0.0"
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Registrar routers
app.include_router(public.router)
app.include_router(admin.router)

@app.exception_handler(401)
async def unauthorized_exception_handler(request: Request, exc: Exception):
    """
    Redirige automáticamente al login de administración cuando falla la sesión del navegador.
    """
    if request.url.path.startswith("/admin") and "/auth/login" not in request.url.path:
        return RedirectResponse(url="/admin/auth/login")
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={"active_page": None},
        status_code=401
    )

# Manejadores de errores HTTP utilizando plantillas Jinja2
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    """
    Manejador personalizado para errores 404 (No Encontrado).
    """
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={"active_page": None},
        status_code=404
    )

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: Exception):
    """
    Manejador personalizado para errores 500 (Error Interno del Servidor).
    """
    return templates.TemplateResponse(
        request=request,
        name="500.html",
        context={"active_page": None},
        status_code=500
    )
