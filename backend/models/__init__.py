from backend.models.base import Base
from backend.models.auth import Usuario, Rol, Permiso, RolPermiso, UsuarioRol, SesionActiva
from backend.models.colegio import Colegio, Noticia, MensajeContacto
from backend.models.academico import Alumno, Matricula
from backend.models.auditoria import RegistroAuditoria

__all__ = [
    "Base",
    "Usuario",
    "Rol",
    "Permiso",
    "RolPermiso",
    "UsuarioRol",
    "SesionActiva",
    "Colegio",
    "Noticia",
    "MensajeContacto",
    "Alumno",
    "Matricula",
    "RegistroAuditoria",
]
