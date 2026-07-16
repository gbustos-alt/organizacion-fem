from fastapi import APIRouter, Request, Depends, Form, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.models import Colegio, MensajeContacto, Noticia, MaterialReflexion, ConfiguracionLema, MemoriaAnual, Alumno

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

    # 3. Contar colegios activos reales y alumnos
    cant_colegios = db.query(Colegio).filter(Colegio.activo == True).count()
    
    # 4. Contar alumnos activos reales
    cant_alumnos = db.query(Alumno).count()
    if cant_alumnos == 0:
        cant_alumnos = 10000  # Fallback a la cifra estimada

    # 5. Obtener lema anual y últimas reflexiones para el recursero de la Home
    lema = db.query(ConfiguracionLema).filter(ConfiguracionLema.activo == True).order_by(ConfiguracionLema.anio.desc()).first()
    latest_resources = db.query(MaterialReflexion).filter(
        MaterialReflexion.activo == True,
        MaterialReflexion.categoria != "Cita Inspiradora"
    ).order_by(MaterialReflexion.fecha_publicacion.desc()).limit(4).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "active_page": "home",
            "novedades": novedades,
            "cita": cita,
            "cant_colegios": cant_colegios,
            "cant_alumnos": cant_alumnos,
            "lema": lema,
            "latest_resources": latest_resources
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

@router.get("/colegios/{colegio_id}", response_class=HTMLResponse)
async def colegio_detalle(colegio_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Ruta para la ficha detallada de un colegio.
    """
    colegio = db.query(Colegio).filter(Colegio.id == colegio_id, Colegio.activo == True).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")
    return templates.TemplateResponse(
        request=request,
        name="colegio_detalle.html",
        context={"active_page": "colegios", "colegio": colegio}
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

@router.get("/trabaja-con-nosotros", response_class=HTMLResponse)
async def trabaja_con_nosotros(request: Request):
    """
    Ruta para la Bolsa de Trabajo institucional.
    """
    return templates.TemplateResponse(
        request=request,
        name="trabaja_con_nosotros.html",
        context={"active_page": "trabaja-con-nosotros"}
    )

@router.post("/trabaja-con-nosotros", response_class=HTMLResponse)
async def submit_trabaja_con_nosotros(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(None),
    area: str = Form(...),
    provincia: str = Form(...),
    mensaje: str = Form(None),
    cv: UploadFile = File(...)
):
    """
    Procesamiento del formulario de Bolsa de Trabajo.
    Simula la recepción del archivo y muestra el estado exitoso.
    """
    return templates.TemplateResponse(
        request=request,
        name="trabaja_con_nosotros.html",
        context={
            "active_page": "trabaja-con-nosotros",
            "success": True
        }
    )

@router.get("/congregaciones", response_class=HTMLResponse)
async def congregaciones(request: Request):
    """
    Ruta para la sección y formulario de Congregaciones.
    """
    return templates.TemplateResponse(
        request=request,
        name="congregaciones.html",
        context={"active_page": "congregaciones"}
    )

@router.post("/congregaciones", response_class=HTMLResponse)
async def submit_congregaciones(
    request: Request,
    congregacion: str = Form(...),
    representante: str = Form(...),
    cargo: str = Form(...),
    email: str = Form(...),
    telefono: str = Form(...),
    motivo: str = Form(...),
    mensaje: str = Form(...)
):
    """
    Procesamiento del formulario de Congregaciones.
    Muestra la vista con el mensaje de éxito.
    """
    return templates.TemplateResponse(
        request=request,
        name="congregaciones.html",
        context={
            "active_page": "congregaciones",
            "success": True
        }
    )


@router.get("/materiales", response_class=HTMLResponse)
async def materiales_publico(
    request: Request,
    buscar: str = None,
    categoria: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(MaterialReflexion).filter(MaterialReflexion.activo == True)
    
    if buscar:
        query = query.filter(
            (MaterialReflexion.titulo.ilike(f"%{buscar}%")) | 
            (MaterialReflexion.autor.ilike(f"%{buscar}%")) |
            (MaterialReflexion.contenido.ilike(f"%{buscar}%"))
        )
        
    if categoria and categoria != "Todos":
        query = query.filter(MaterialReflexion.categoria == categoria)
        
    materiales = query.order_by(MaterialReflexion.fecha_publicacion.desc()).all()
    
    # Categorías disponibles para filtros
    categorias = ["Todos", "Pedagógico", "Pastoral", "Editorial", "Cita Inspiradora"]
    
    return templates.TemplateResponse(
        request=request,
        name="materiales.html",
        context={
            "active_page": "materiales",
            "materiales": materiales,
            "buscar": buscar,
            "categoria": categoria or "Todos",
            "categorias": categorias
        }
    )


@router.get("/memorias", response_class=HTMLResponse)
async def memorias_publicas(request: Request, db: Session = Depends(get_db)):
    memorias = db.query(MemoriaAnual).filter(MemoriaAnual.activo == True).order_by(MemoriaAnual.anio.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="memorias.html",
        context={
            "active_page": "memorias",
            "memorias": memorias
        }
    )
