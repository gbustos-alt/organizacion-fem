from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import Colegio
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/colegios", tags=["admin-colegios"])

def validar_scope_colegio(colegio_id: int, request: Request):
    scopes = getattr(request.state, "colegios_permitidos", [])
    if None in scopes:  # Scope Global
        return True
    if colegio_id in scopes:  # Scope Colegio Local
        return True
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Acceso denegado: No tiene permisos sobre este colegio."
    )

@router.get("/", response_class=HTMLResponse)
async def listar_colegios(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("colegio", "leer"))
):
    scopes = request.state.colegios_permitidos
    query = db.query(Colegio)
    if None not in scopes:
        query = query.filter(Colegio.id.in_(scopes))
    
    colegios = query.all()
    return templates.TemplateResponse(
        request=request,
        name="admin/colegios/list.html",
        context={"user": user, "active_page": "colegios", "colegios": colegios}
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_colegio_form(
    request: Request,
    user = Depends(RequerirPermiso("colegio", "crear"))
):
    # Solo administradores globales pueden crear colegios en el sistema
    scopes = request.state.colegios_permitidos
    if None not in scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida: Solo directivos de la fundación pueden crear nuevos colegios."
        )

    return templates.TemplateResponse(
        request=request,
        name="admin/colegios/form.html",
        context={"user": user, "active_page": "colegios", "colegio": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_colegio_submit(
    request: Request,
    nombre: str = Form(...),
    ubicacion: str = Form(None),
    congregacion: str = Form(None),
    diocesis: str = Form(None),
    telefono: str = Form(None),
    web_url: str = Form(None),
    descripcion: str = Form(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("colegio", "crear"))
):
    scopes = request.state.colegios_permitidos
    if None not in scopes:
        raise HTTPException(status_code=403, detail="Operación restringida.")

    nuevo_colegio = Colegio(
        nombre=nombre,
        ubicacion=ubicacion,
        congregacion=congregacion,
        diocesis=diocesis,
        telefono=telefono,
        web_url=web_url,
        descripcion=descripcion
    )
    db.add(nuevo_colegio)
    db.commit()
    db.refresh(nuevo_colegio)

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="colegio",
        recurso_id=nuevo_colegio.id,
        colegio_id=nuevo_colegio.id,
        valores_nuevos={"nombre": nombre, "ubicacion": ubicacion}
    )

    return RedirectResponse(url="/admin/colegios/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar/{colegio_id}", response_class=HTMLResponse)
async def editar_colegio_form(
    colegio_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("colegio", "editar"))
):
    validar_scope_colegio(colegio_id, request)
    colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    return templates.TemplateResponse(
        request=request,
        name="admin/colegios/form.html",
        context={"user": user, "active_page": "colegios", "colegio": colegio}
    )

@router.post("/editar/{colegio_id}", response_class=HTMLResponse)
async def editar_colegio_submit(
    colegio_id: int,
    request: Request,
    nombre: str = Form(...),
    ubicacion: str = Form(None),
    congregacion: str = Form(None),
    diocesis: str = Form(None),
    telefono: str = Form(None),
    web_url: str = Form(None),
    descripcion: str = Form(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("colegio", "editar"))
):
    validar_scope_colegio(colegio_id, request)
    colegio = db.query(Colegio).filter(Colegio.id == colegio_id).first()
    if not colegio:
        raise HTTPException(status_code=404, detail="Colegio no encontrado")

    valores_anteriores = {
        "nombre": colegio.nombre,
        "ubicacion": colegio.ubicacion,
    }

    colegio.nombre = nombre
    colegio.ubicacion = ubicacion
    colegio.congregacion = congregacion
    colegio.diocesis = diocesis
    colegio.telefono = telefono
    colegio.web_url = web_url
    colegio.descripcion = descripcion
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="colegio",
        recurso_id=colegio.id,
        colegio_id=colegio.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"nombre": nombre, "ubicacion": ubicacion}
    )

    return RedirectResponse(url="/admin/colegios/", status_code=status.HTTP_303_SEE_OTHER)
