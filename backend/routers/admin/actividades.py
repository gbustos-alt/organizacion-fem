from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import datetime
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import Actividad
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/actividades", tags=["admin-actividades"])

@router.get("/", response_class=HTMLResponse)
async def listar_actividades(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("actividad", "leer"))
):
    actividades = db.query(Actividad).order_by(Actividad.fecha.asc()).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/actividades/list.html",
        context={"user": user, "active_page": "actividades", "actividades": actividades}
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_actividad_form(
    request: Request,
    user = Depends(RequerirPermiso("actividad", "crear"))
):
    return templates.TemplateResponse(
        request=request,
        name="admin/actividades/form.html",
        context={"user": user, "active_page": "actividades", "actividad": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_actividad_submit(
    request: Request,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    fecha: str = Form(...),  # Formato YYYY-MM-DDTHH:MM
    lugar: str = Form("Virtual"),
    destinatarios: str = Form(None),
    link_inscripcion: str = Form(None),
    activa: bool = Form(True),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("actividad", "crear"))
):
    try:
        fecha_dt = datetime.datetime.fromisoformat(fecha)
    except ValueError:
        return templates.TemplateResponse(
            request=request,
            name="admin/actividades/form.html",
            context={
                "user": user,
                "active_page": "actividades",
                "actividad": None,
                "error": "Formato de fecha inválido."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    nueva_actividad = Actividad(
        titulo=titulo,
        descripcion=descripcion,
        fecha=fecha_dt,
        lugar=lugar,
        destinatarios=destinatarios,
        link_inscripcion=link_inscripcion,
        activa=activa
    )
    db.add(nueva_actividad)
    db.commit()
    db.refresh(nueva_actividad)

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="actividad",
        recurso_id=nueva_actividad.id,
        valores_nuevos={"titulo": titulo, "fecha": fecha}
    )

    return RedirectResponse(url="/admin/actividades/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar/{actividad_id}", response_class=HTMLResponse)
async def editar_actividad_form(
    actividad_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("actividad", "editar"))
):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    return templates.TemplateResponse(
        request=request,
        name="admin/actividades/form.html",
        context={"user": user, "active_page": "actividades", "actividad": actividad}
    )

@router.post("/editar/{actividad_id}", response_class=HTMLResponse)
async def editar_actividad_submit(
    actividad_id: int,
    request: Request,
    titulo: str = Form(...),
    descripcion: str = Form(...),
    fecha: str = Form(...),
    lugar: str = Form("Virtual"),
    destinatarios: str = Form(None),
    link_inscripcion: str = Form(None),
    activa: bool = Form(False),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("actividad", "editar"))
):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    try:
        fecha_dt = datetime.datetime.fromisoformat(fecha)
    except ValueError:
        return templates.TemplateResponse(
            request=request,
            name="admin/actividades/form.html",
            context={
                "user": user,
                "active_page": "actividades",
                "actividad": actividad,
                "error": "Formato de fecha inválido."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    valores_anteriores = {
        "titulo": actividad.titulo,
        "fecha": actividad.fecha.isoformat(),
    }

    actividad.titulo = titulo
    actividad.descripcion = descripcion
    actividad.fecha = fecha_dt
    actividad.lugar = lugar
    actividad.destinatarios = destinatarios
    actividad.link_inscripcion = link_inscripcion
    actividad.activa = activa
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="actividad",
        recurso_id=actividad.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"titulo": titulo, "fecha": fecha}
    )

    return RedirectResponse(url="/admin/actividades/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/eliminar/{actividad_id}")
async def eliminar_actividad(
    actividad_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("actividad", "eliminar"))
):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    db.delete(actividad)
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="eliminar",
        recurso="actividad",
        recurso_id=actividad_id,
        valores_anteriores={"titulo": actividad.titulo}
    )

    return RedirectResponse(url="/admin/actividades/", status_code=status.HTTP_303_SEE_OTHER)
