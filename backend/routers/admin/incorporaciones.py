import datetime
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import AuditoriaIncorporacion, Colegio, Rol, UsuarioRol
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/incorporaciones", tags=["admin-incorporaciones"])

def obtener_roles_usuario(db: Session, usuario_id: int):
    roles = db.query(Rol).join(UsuarioRol).filter(UsuarioRol.usuario_id == usuario_id).all()
    return [r.nombre for r in roles]

def verificar_permiso_edicion_area(user_roles: list, area: str) -> bool:
    if "Administrador General" in user_roles:
        return True
    if area == "pedagogica" and "Auditor Pedagógico" in user_roles:
        return True
    if area == "pastoral" and "Auditor Pastoral" in user_roles:
        return True
    if area == "economica" and "Auditor Económico" in user_roles:
        return True
    if area == "legal" and "Auditor Legal" in user_roles:
        return True
    return False

@router.get("/", response_class=HTMLResponse)
async def listar_incorporaciones(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("auditoria_incorporacion", "leer"))
):
    incorporaciones = db.query(AuditoriaIncorporacion).order_by(AuditoriaIncorporacion.created_at.desc()).all()
    user_roles = obtener_roles_usuario(db, user.id)
    
    return templates.TemplateResponse(
        request=request,
        name="admin/incorporaciones/list.html",
        context={
            "user": user,
            "active_page": "incorporaciones",
            "incorporaciones": incorporaciones,
            "user_roles": user_roles
        }
    )

@router.get("/crear", response_class=HTMLResponse)
async def crear_candidato_form(
    request: Request,
    user = Depends(RequerirPermiso("auditoria_incorporacion", "crear"))
):
    return templates.TemplateResponse(
        request=request,
        name="admin/incorporaciones/form.html",
        context={"user": user, "active_page": "incorporaciones", "candidato": None}
    )

@router.post("/crear", response_class=HTMLResponse)
async def crear_candidato_submit(
    request: Request,
    nombre: str = Form(...),
    congregacion: str = Form(None),
    diocesis: str = Form(None),
    localidad: str = Form(None),
    provincia: str = Form("Presencia Federal"),
    drive_folder_url: str = Form(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("auditoria_incorporacion", "crear"))
):
    nuevo_candidato = AuditoriaIncorporacion(
        nombre=nombre.strip(),
        congregacion=congregacion.strip() if congregacion else None,
        diocesis=diocesis.strip() if diocesis else None,
        localidad=localidad.strip() if localidad else None,
        provincia=provincia,
        drive_folder_url=drive_folder_url.strip() if drive_folder_url else None,
        estado="PENDIENTE",
        estado_pedagogica="PENDIENTE",
        estado_pastoral="PENDIENTE",
        estado_economica="PENDIENTE",
        estado_legal="PENDIENTE"
    )
    
    db.add(nuevo_candidato)
    db.flush()
    
    # Registrar auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="auditoria_incorporacion",
        recurso_id=nuevo_candidato.id,
        valores_nuevos={
            "nombre": nuevo_candidato.nombre,
            "localidad": nuevo_candidato.localidad,
            "provincia": nuevo_candidato.provincia,
            "drive_folder_url": nuevo_candidato.drive_folder_url
        }
    )
    
    db.commit()
    return RedirectResponse(url="/admin/incorporaciones/", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/detalle/{candidato_id}", response_class=HTMLResponse)
async def detalle_incorporacion(
    candidato_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("auditoria_incorporacion", "leer"))
):
    candidato = db.query(AuditoriaIncorporacion).filter(AuditoriaIncorporacion.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
        
    user_roles = obtener_roles_usuario(db, user.id)
    
    # Resolver permisos específicos de área
    can_edit_pedagogica = verificar_permiso_edicion_area(user_roles, "pedagogica")
    can_edit_pastoral = verificar_permiso_edicion_area(user_roles, "pastoral")
    can_edit_economica = verificar_permiso_edicion_area(user_roles, "economica")
    can_edit_legal = verificar_permiso_edicion_area(user_roles, "legal")
    
    can_approve = "Administrador General" in user_roles
    
    return templates.TemplateResponse(
        request=request,
        name="admin/incorporaciones/detail.html",
        context={
            "user": user,
            "active_page": "incorporaciones",
            "candidato": candidato,
            "user_roles": user_roles,
            "can_edit_pedagogica": can_edit_pedagogica,
            "can_edit_pastoral": can_edit_pastoral,
            "can_edit_economica": can_edit_economica,
            "can_edit_legal": can_edit_legal,
            "can_approve": can_approve
        }
    )

@router.post("/editar/{candidato_id}", response_class=HTMLResponse)
async def editar_incorporacion_submit(
    candidato_id: int,
    request: Request,
    drive_folder_url: str = Form(None),
    estado_pedagogica: str = Form(None),
    obs_pedagogica: str = Form(None),
    estado_pastoral: str = Form(None),
    obs_pastoral: str = Form(None),
    estado_economica: str = Form(None),
    obs_economica: str = Form(None),
    estado_legal: str = Form(None),
    obs_legal: str = Form(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("auditoria_incorporacion", "editar"))
):
    candidato = db.query(AuditoriaIncorporacion).filter(AuditoriaIncorporacion.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
        
    user_roles = obtener_roles_usuario(db, user.id)
    valores_anteriores = {
        "estado_pedagogica": candidato.estado_pedagogica,
        "obs_pedagogica": candidato.obs_pedagogica,
        "estado_pastoral": candidato.estado_pastoral,
        "obs_pastoral": candidato.obs_pastoral,
        "estado_economica": candidato.estado_economica,
        "obs_economica": candidato.obs_economica,
        "estado_legal": candidato.estado_legal,
        "obs_legal": candidato.obs_legal,
        "drive_folder_url": candidato.drive_folder_url,
        "estado": candidato.estado
    }
    
    # 1. Modificación de campos restringidos según rol
    cambios = {}
    
    if verificar_permiso_edicion_area(user_roles, "pedagogica") and estado_pedagogica:
        candidato.estado_pedagogica = estado_pedagogica
        candidato.obs_pedagogica = obs_pedagogica.strip() if obs_pedagogica else None
        cambios["estado_pedagogica"] = estado_pedagogica
        cambios["obs_pedagogica"] = candidato.obs_pedagogica
        
    if verificar_permiso_edicion_area(user_roles, "pastoral") and estado_pastoral:
        candidato.estado_pastoral = estado_pastoral
        candidato.obs_pastoral = obs_pastoral.strip() if obs_pastoral else None
        cambios["estado_pastoral"] = estado_pastoral
        cambios["obs_pastoral"] = candidato.obs_pastoral
        
    if verificar_permiso_edicion_area(user_roles, "economica") and estado_economica:
        candidato.estado_economica = estado_economica
        candidato.obs_economica = obs_economica.strip() if obs_economica else None
        cambios["estado_economica"] = estado_economica
        cambios["obs_economica"] = candidato.obs_economica
        
    if verificar_permiso_edicion_area(user_roles, "legal") and estado_legal:
        candidato.estado_legal = estado_legal
        candidato.obs_legal = obs_legal.strip() if obs_legal else None
        cambios["estado_legal"] = estado_legal
        cambios["obs_legal"] = candidato.obs_legal

    # Modificación general de la carpeta de Drive
    if "Administrador General" in user_roles or any(r.startswith("Auditor") for r in user_roles):
        candidato.drive_folder_url = drive_folder_url.strip() if drive_folder_url else None
        cambios["drive_folder_url"] = candidato.drive_folder_url

    # Actualizar estado global automáticamente según el avance
    estados_areas = [candidato.estado_pedagogica, candidato.estado_pastoral, candidato.estado_economica, candidato.estado_legal]
    if any(e == "OBSERVADO" for e in estados_areas):
        candidato.estado = "EN_PROCESO"
    elif all(e == "COMPLETADO" for e in estados_areas):
        candidato.estado = "EN_PROCESO"  # Aún requiere aprobación manual
    elif any(e == "EN_PROCESO" for e in estados_areas) or any(e == "COMPLETADO" for e in estados_areas):
        candidato.estado = "EN_PROCESO"
    else:
        candidato.estado = "PENDIENTE"
        
    db.flush()
    
    # Registrar auditoría
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="auditoria_incorporacion",
        recurso_id=candidato.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos=cambios
    )
    
    db.commit()
    return RedirectResponse(url=f"/admin/incorporaciones/detalle/{candidato_id}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/aprobar/{candidato_id}", response_class=HTMLResponse)
async def aprobar_incorporacion(
    candidato_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("auditoria_incorporacion", "aprobar"))
):
    candidato = db.query(AuditoriaIncorporacion).filter(AuditoriaIncorporacion.id == candidato_id).first()
    if not candidato:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
        
    user_roles = obtener_roles_usuario(db, user.id)
    if "Administrador General" not in user_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación restringida: Solo el Administrador General de la Fundación puede aprobar incorporaciones."
        )
        
    # 1. Crear el Colegio Activo Oficial
    nuevo_colegio = Colegio(
        nombre=candidato.nombre,
        congregacion=candidato.congregacion,
        diocesis=candidato.diocesis,
        ubicacion=candidato.localidad,
        provincia=candidato.provincia,
        activo=True
    )
    db.add(nuevo_colegio)
    db.flush()
    
    # 2. Marcar la auditoría como APROBADA
    candidato.estado = "APROBADA"
    candidato.estado_pedagogica = "COMPLETADO"
    candidato.estado_pastoral = "COMPLETADO"
    candidato.estado_economica = "COMPLETADO"
    candidato.estado_legal = "COMPLETADO"
    
    # 3. Registrar auditoría de aprobación
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="aprobar",
        recurso="auditoria_incorporacion",
        recurso_id=candidato.id,
        valores_nuevos={"estado": "APROBADA", "colegio_id_creado": nuevo_colegio.id}
    )
    
    db.commit()
    return RedirectResponse(url="/admin/colegios/", status_code=status.HTTP_303_SEE_OTHER)
