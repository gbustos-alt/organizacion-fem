from backend.models.base import Base
from backend.models.auth import Usuario, Rol, Permiso, RolPermiso, UsuarioRol, SesionActiva
from backend.models.colegio import Colegio, Noticia, MensajeContacto, MaterialReflexion, Actividad
from backend.models.academico import Alumno, Matricula
from backend.models.auditoria import RegistroAuditoria
from backend.models.incorporacion import AuditoriaIncorporacion
from backend.models.configuracion import ConfiguracionLema, MemoriaAnual, MaterialCapacitacion

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
    "MaterialReflexion",
    "Actividad",
    "Alumno",
    "Matricula",
    "RegistroAuditoria",
    "AuditoriaIncorporacion",
    "ConfiguracionLema",
    "MemoriaAnual",
    "MaterialCapacitacion",
]
