from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import datetime
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import MaterialReflexion
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/materiales", tags=["admin-materiales"])

@router.get("/", response_class=HTMLResponse)
async def listar_materiales(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("material_reflexion", "leer"))
):
    materiales = db.query(MaterialReflexion).order_by(MaterialReflexion.fecha_publicacion.desc()).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/materiales/list.html",
        context={"user": user, "active_page": "materiales", "materiales": materiales}
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_material_form(
    request: Request,
    user = Depends(RequerirPermiso("material_reflexion", "crear"))
):
    return templates.TemplateResponse(
        request=request,
        name="admin/materiales/form.html",
        context={"user": user, "active_page": "materiales", "material": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_material_submit(
    request: Request,
    titulo: str = Form(...),
    autor: str = Form("Fundación FEM"),
    categoria: str = Form(...),
    contenido: str = Form(None),
    archivo_url: str = Form(None),
    link_url: str = Form(None),
    activo: bool = Form(True),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("material_reflexion", "crear"))
):
    nuevo_material = MaterialReflexion(
        titulo=titulo,
        autor=autor,
        categoria=categoria,
        contenido=contenido,
        archivo_url=archivo_url,
        link_url=link_url,
        activo=activo,
        fecha_publicacion=datetime.datetime.utcnow()
    )
    db.add(nuevo_material)
    db.commit()
    db.refresh(nuevo_material)

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="material_reflexion",
        recurso_id=nuevo_material.id,
        valores_nuevos={"titulo": titulo, "categoria": categoria}
    )

    return RedirectResponse(url="/admin/materiales/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar/{material_id}", response_class=HTMLResponse)
async def editar_material_form(
    material_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("material_reflexion", "editar"))
):
    material = db.query(MaterialReflexion).filter(MaterialReflexion.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    return templates.TemplateResponse(
        request=request,
        name="admin/materiales/form.html",
        context={"user": user, "active_page": "materiales", "material": material}
    )

@router.post("/editar/{material_id}", response_class=HTMLResponse)
async def editar_material_submit(
    material_id: int,
    request: Request,
    titulo: str = Form(...),
    autor: str = Form("Fundación FEM"),
    categoria: str = Form(...),
    contenido: str = Form(None),
    archivo_url: str = Form(None),
    link_url: str = Form(None),
    activo: bool = Form(False),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("material_reflexion", "editar"))
):
    material = db.query(MaterialReflexion).filter(MaterialReflexion.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    valores_anteriores = {
        "titulo": material.titulo,
        "categoria": material.categoria,
    }

    material.titulo = titulo
    material.autor = autor
    material.categoria = categoria
    material.contenido = contenido
    material.archivo_url = archivo_url
    material.link_url = link_url
    material.activo = activo
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="material_reflexion",
        recurso_id=material.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"titulo": titulo, "categoria": categoria}
    )

    return RedirectResponse(url="/admin/materiales/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/eliminar/{material_id}")
async def eliminar_material(
    material_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("material_reflexion", "eliminar"))
):
    material = db.query(MaterialReflexion).filter(MaterialReflexion.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    db.delete(material)
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="eliminar",
        recurso="material_reflexion",
        recurso_id=material_id,
        valores_anteriores={"titulo": material.titulo}
    )

    return RedirectResponse(url="/admin/materiales/", status_code=status.HTTP_303_SEE_OTHER)
