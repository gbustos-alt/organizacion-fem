from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import datetime
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import Noticia
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/novedades", tags=["admin-novedades"])

@router.get("/", response_class=HTMLResponse)
async def listar_novedades(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("novedad", "leer"))
):
    novedades = db.query(Noticia).order_by(Noticia.fecha_publicacion.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/novedades/list.html",
        context={"user": user, "active_page": "novedades", "novedades": novedades}
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_novedad_form(
    request: Request,
    user = Depends(RequerirPermiso("novedad", "crear"))
):
    return templates.TemplateResponse(
        request=request,
        name="admin/novedades/form.html",
        context={"user": user, "active_page": "novedades", "novedad": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_novedad_submit(
    request: Request,
    titulo: str = Form(...),
    copete: str = Form(None),
    contenido: str = Form(...),
    imagen_url: str = Form(None),
    activa: bool = Form(True),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("novedad", "crear"))
):
    nueva_novedad = Noticia(
        titulo=titulo,
        copete=copete,
        contenido=contenido,
        imagen_url=imagen_url,
        activa=activa,
        fecha_publicacion=datetime.datetime.utcnow()
    )
    db.add(nueva_novedad)
    db.commit()
    db.refresh(nueva_novedad)

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="novedad",
        recurso_id=nueva_novedad.id,
        valores_nuevos={"titulo": titulo, "activa": activa}
    )

    return RedirectResponse(url="/admin/novedades/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar/{novedad_id}", response_class=HTMLResponse)
async def editar_novedad_form(
    novedad_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("novedad", "editar"))
):
    novedad = db.query(Noticia).filter(Noticia.id == novedad_id).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada")

    return templates.TemplateResponse(
        request=request,
        name="admin/novedades/form.html",
        context={"user": user, "active_page": "novedades", "novedad": novedad}
    )

@router.post("/editar/{novedad_id}", response_class=HTMLResponse)
async def editar_novedad_submit(
    novedad_id: int,
    request: Request,
    titulo: str = Form(...),
    copete: str = Form(None),
    contenido: str = Form(...),
    imagen_url: str = Form(None),
    activa: bool = Form(False),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("novedad", "editar"))
):
    novedad = db.query(Noticia).filter(Noticia.id == novedad_id).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada")

    valores_anteriores = {
        "titulo": novedad.titulo,
        "activa": novedad.activa,
    }

    novedad.titulo = titulo
    novedad.copete = copete
    novedad.contenido = contenido
    novedad.imagen_url = imagen_url
    novedad.activa = activa
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="novedad",
        recurso_id=novedad.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"titulo": titulo, "activa": activa}
    )

    return RedirectResponse(url="/admin/novedades/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/eliminar/{novedad_id}")
async def eliminar_novedad(
    novedad_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("novedad", "eliminar"))
):
    novedad = db.query(Noticia).filter(Noticia.id == novedad_id).first()
    if not novedad:
        raise HTTPException(status_code=404, detail="Novedad no encontrada")

    db.delete(novedad)
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="eliminar",
        recurso="novedad",
        recurso_id=novedad_id,
        valores_anteriores={"titulo": novedad.titulo}
    )

    return RedirectResponse(url="/admin/novedades/", status_code=status.HTTP_303_SEE_OTHER)
