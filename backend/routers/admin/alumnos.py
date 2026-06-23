from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import Alumno, Colegio
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/alumnos", tags=["admin-alumnos"])

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
async def listar_alumnos(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "leer"))
):
    scopes = request.state.colegios_permitidos
    query = db.query(Alumno)
    if None not in scopes:
        query = query.filter(Alumno.colegio_id.in_(scopes))
        
    alumnos = query.all()
    return templates.TemplateResponse(
        request=request,
        name="admin/alumnos/list.html",
        context={"user": user, "active_page": "alumnos", "alumnos": alumnos}
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_alumno_form(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "crear"))
):
    scopes = request.state.colegios_permitidos
    query_colegios = db.query(Colegio)
    if None not in scopes:
        query_colegios = query_colegios.filter(Colegio.id.in_(scopes))
        
    colegios = query_colegios.all()
    return templates.TemplateResponse(
        request=request,
        name="admin/alumnos/form.html",
        context={"user": user, "active_page": "alumnos", "colegio": None, "colegios": colegios, "alumno": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_alumno_submit(
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    documento: str = Form(...),
    colegio_id: int = Form(...),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "crear"))
):
    validar_scope_colegio(colegio_id, request)
    
    # Validar documento único
    existente = db.query(Alumno).filter(Alumno.documento == documento).first()
    if existente:
        query_colegios = db.query(Colegio)
        scopes = request.state.colegios_permitidos
        if None not in scopes:
            query_colegios = query_colegios.filter(Colegio.id.in_(scopes))
        
        return templates.TemplateResponse(
            request=request,
            name="admin/alumnos/form.html",
            context={
                "user": user,
                "active_page": "alumnos",
                "colegios": query_colegios.all(),
                "alumno": None,
                "error": f"Ya existe un alumno con el documento {documento}."
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )

    nuevo_alumno = Alumno(
        nombre=nombre,
        apellido=apellido,
        documento=documento,
        colegio_id=colegio_id
    )
    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)

    # Registrar acción en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="alumno",
        recurso_id=nuevo_alumno.id,
        colegio_id=colegio_id,
        valores_nuevos={"nombre": nombre, "apellido": apellido, "documento": documento, "colegio_id": colegio_id}
    )

    return RedirectResponse(url="/admin/alumnos/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar/{alumno_id}", response_class=HTMLResponse)
async def editar_alumno_form(
    alumno_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "editar"))
):
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
    validar_scope_colegio(alumno.colegio_id, request)
    
    scopes = request.state.colegios_permitidos
    query_colegios = db.query(Colegio)
    if None not in scopes:
        query_colegios = query_colegios.filter(Colegio.id.in_(scopes))
        
    colegios = query_colegios.all()
    return templates.TemplateResponse(
        request=request,
        name="admin/alumnos/form.html",
        context={"user": user, "active_page": "alumnos", "colegios": colegios, "alumno": alumno}
    )

@router.post("/editar/{alumno_id}", response_class=HTMLResponse)
async def editar_alumno_submit(
    alumno_id: int,
    request: Request,
    nombre: str = Form(...),
    apellido: str = Form(...),
    documento: str = Form(...),
    colegio_id: int = Form(...),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "editar"))
):
    alumno = db.query(Alumno).filter(Alumno.id == alumno_id).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
        
    validar_scope_colegio(alumno.colegio_id, request)  # Validar scope del colegio anterior
    validar_scope_colegio(colegio_id, request)        # Validar scope del colegio nuevo
    
    valores_anteriores = {
        "nombre": alumno.nombre,
        "apellido": alumno.apellido,
        "documento": alumno.documento,
        "colegio_id": alumno.colegio_id
    }

    alumno.nombre = nombre
    alumno.apellido = apellido
    alumno.documento = documento
    alumno.colegio_id = colegio_id
    db.commit()

    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="alumno",
        recurso_id=alumno.id,
        colegio_id=colegio_id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"nombre": nombre, "apellido": apellido, "documento": documento, "colegio_id": colegio_id}
    )

    return RedirectResponse(url="/admin/alumnos/", status_code=status.HTTP_303_SEE_OTHER)
