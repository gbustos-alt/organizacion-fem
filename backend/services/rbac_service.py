from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models import Usuario, UsuarioRol, RolPermiso, Permiso
from backend.services.auth_service import obtener_usuario_de_sesion

def obtener_usuario_actual(request: Request, db: Session = Depends(get_db)) -> Usuario:
    """
    Dependency to retrieve the currently logged-in user from the session cookie.
    """
    session_token = request.cookies.get("session_id")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado. Por favor inicie sesión."
        )
    
    usuario = obtener_usuario_de_sesion(db, session_token)
    if not usuario or not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o usuario inactivo."
        )
    return usuario


class RequerirPermiso:
    """
    FastAPI dependency to verify if a user has a specific permission
    and resolve their school (colegio) scope.
    """
    def __init__(self, recurso: str, accion: str):
        self.recurso = recurso
        self.accion = accion

    def __call__(
        self,
        request: Request,
        user: Usuario = Depends(obtener_usuario_actual),
        db: Session = Depends(get_db)
    ) -> Usuario:
        # Obtener los roles del usuario
        roles_usuario = db.query(UsuarioRol).filter(UsuarioRol.usuario_id == user.id).all()
        
        colegios_permitidos = []
        tiene_permiso = False
        
        for user_rol in roles_usuario:
            # Buscar si el rol de esta asignación tiene el permiso requerido (o comodín '*')
            permisos_rol = db.query(RolPermiso).join(Permiso).filter(
                RolPermiso.rol_id == user_rol.rol_id
            ).all()
            
            for rp in permisos_rol:
                p = rp.permiso
                match_recurso = (p.recurso == self.recurso or p.recurso == "*")
                match_accion = (p.accion == self.accion or p.accion == "*")
                
                if match_recurso and match_accion:
                    tiene_permiso = True
                    colegios_permitidos.append(user_rol.colegio_id)
                    break
        
        if not tiene_permiso:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado: carece del permiso ({self.recurso}:{self.accion})"
            )
        
        # Guardar en request.state para uso en los controladores
        # Lista que contiene:
        # - None (si tiene acceso a nivel Fundación / Global)
        # - [id1, id2...] (si está limitado a colegios específicos)
        request.state.colegios_permitidos = colegios_permitidos
        request.state.usuario = user
        return user
