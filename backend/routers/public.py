from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from backend.core.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Ruta para la página de inicio institucional.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"}
    )

@router.get("/identidad", response_class=HTMLResponse)
async def identidad(request: Request):
    """
    Ruta para la página de Identidad de la institución.
    """
    return templates.TemplateResponse(
        request=request,
        name="identidad.html",
        context={"active_page": "identidad"}
    )

@router.get("/mision", response_class=HTMLResponse)
async def mision(request: Request):
    """
    Ruta para la página de Misión y Visión de la institución.
    """
    return templates.TemplateResponse(
        request=request,
        name="mision.html",
        context={"active_page": "mision"}
    )

@router.get("/dimensiones", response_class=HTMLResponse)
async def dimensiones(request: Request):
    """
    Ruta para la página de Dimensiones del Acompañamiento.
    """
    return templates.TemplateResponse(
        request=request,
        name="dimensiones.html",
        context={"active_page": "dimensiones"}
    )

@router.get("/organizacion", response_class=HTMLResponse)
async def organizacion(request: Request):
    """
    Ruta para la página de Organización y Estructura.
    """
    return templates.TemplateResponse(
        request=request,
        name="organizacion.html",
        context={"active_page": "organizacion"}
    )

@router.get("/colegios", response_class=HTMLResponse)
async def colegios(request: Request):
    """
    Ruta para la página de Colegios Acompañados.
    """
    return templates.TemplateResponse(
        request=request,
        name="colegios.html",
        context={"active_page": "colegios"}
    )

@router.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    """
    Ruta para la página de Contacto Institucional.
    """
    return templates.TemplateResponse(
        request=request,
        name="contacto.html",
        context={"active_page": "contacto"}
    )
