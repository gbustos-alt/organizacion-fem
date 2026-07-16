from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session, joinedload
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import Usuario, Rol, Colegio, UsuarioRol
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/usuarios", tags=["admin-usuarios"])

@router.get("/", response_class=HTMLResponse)
async def listar_usuarios(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("usuario", "leer"))
):
    # Eager load roles_asignados and their associated roles and schools to avoid N+1 query problem
    usuarios = db.query(Usuario).options(
        joinedload(Usuario.roles_asignados).joinedload(UsuarioRol.rol),
        joinedload(Usuario.roles_asignados).joinedload(UsuarioRol.colegio)
    ).order_by(Usuario.created_at.desc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="admin/usuarios/list.html",
        context={"user": user, "active_page": "usuarios", "usuarios": usuarios}
    )

@router.get("/editar/{usuario_id}", response_class=HTMLResponse)
async def editar_usuario_form(
    usuario_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("usuario", "editar"))
):
    usuario_editar = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_editar:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    roles = db.query(Rol).all()
    colegios = db.query(Colegio).filter(Colegio.activo == True).all()
    
    # Obtener el rol y scope actual del usuario
    rol_actual_id = None
    colegio_actual_id = None
    if usuario_editar.roles_asignados:
        rol_actual_id = usuario_editar.roles_asignados[0].rol_id
        colegio_actual_id = usuario_editar.roles_asignados[0].colegio_id
        
    return templates.TemplateResponse(
        request=request,
        name="admin/usuarios/form.html",
        context={
            "user": user,
            "active_page": "usuarios",
            "usuario": usuario_editar,
            "roles": roles,
            "colegios": colegios,
            "rol_actual_id": rol_actual_id,
            "colegio_actual_id": colegio_actual_id
        }
    )

@router.post("/editar/{usuario_id}", response_class=HTMLResponse)
async def editar_usuario_submit(
    usuario_id: int,
    request: Request,
    rol_id: int = Form(...),
    colegio_id: str = Form(""),  # "" representa Global (None)
    activo: bool = Form(False),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("usuario", "editar"))
):
    usuario_editar = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario_editar:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    # Impedir que un administrador se desactive a sí mismo
    if usuario_editar.id == user.id and not activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operación inválida: No puede desactivar su propio usuario administrador."
        )
        
    valores_anteriores = {
        "activo": usuario_editar.activo,
        "rol_id": usuario_editar.roles_asignados[0].rol_id if usuario_editar.roles_asignados else None,
        "colegio_id": usuario_editar.roles_asignados[0].colegio_id if usuario_editar.roles_asignados else None
    }
    
    # 1. Actualizar estado activo
    usuario_editar.activo = activo
    
    # 2. Actualizar roles y scopes
    # Limpiar asignaciones previas
    db.query(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id).delete()
    
    # Crear nueva asignación
    db_colegio_id = int(colegio_id) if (colegio_id and colegio_id.isdigit()) else None
    nueva_asignacion = UsuarioRol(
        usuario_id=usuario_id,
        rol_id=rol_id,
        colegio_id=db_colegio_id
    )
    db.add(nueva_asignacion)
    db.flush()
    
    # Registrar en auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="usuario",
        recurso_id=usuario_id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"activo": activo, "rol_id": rol_id, "colegio_id": db_colegio_id}
    )
    
    db.commit()
    return RedirectResponse(url="/admin/usuarios/", status_code=status.HTTP_303_SEE_OTHER)
