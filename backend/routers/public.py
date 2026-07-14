from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.models import Colegio, MensajeContacto, Noticia, MaterialReflexion

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Ruta para la página de inicio institucional.
    """
    # 1. Obtener las últimas 3 noticias activas
    novedades = db.query(Noticia).filter(Noticia.activa == True).order_by(Noticia.fecha_publicacion.desc()).limit(3).all()

    # 2. Obtener la última cita de reflexión activa
    cita = db.query(MaterialReflexion).filter(
        MaterialReflexion.activo == True,
        MaterialReflexion.categoria == "Cita Inspiradora"
    ).order_by(MaterialReflexion.fecha_publicacion.desc()).first()

    # 3. Contar colegios activos reales
    cant_colegios = db.query(Colegio).filter(Colegio.activo == True).count()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "active_page": "home",
            "novedades": novedades,
            "cita": cita,
            "cant_colegios": cant_colegios
        }
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
async def colegios(request: Request, db: Session = Depends(get_db)):
    """
    Ruta para la página de Colegios Acompañados.
    """
    listado_colegios = db.query(Colegio).all()
    return templates.TemplateResponse(
        request=request,
        name="colegios.html",
        context={"active_page": "colegios", "colegios": listado_colegios}
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

@router.post("/contacto", response_class=HTMLResponse)
async def submit_contacto(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    mensaje: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint para procesar el formulario de contacto e insertarlo en la DB.
    """
    nuevo_mensaje = MensajeContacto(
        nombre=nombre,
        email=email,
        telefono=telefono,
        mensaje=mensaje
    )
    db.add(nuevo_mensaje)
    db.commit()
    return templates.TemplateResponse(
        request=request,
        name="contacto.html",
        context={
            "active_page": "contacto",
            "success": True,
            "mensaje_exito": "¡Gracias por contactarte con nosotros! Hemos recibido tu mensaje."
        }
    )

