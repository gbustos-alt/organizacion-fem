import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.models.base import Base

class Usuario(Base):
    """
    Representa a cualquier actor que interactúa con el sistema (Humanos y Agentes).
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    tipo = Column(String(20), default="HUMANO", nullable=False)  # "HUMANO" o "AGENTE"
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relación con sus asignaciones de roles
    roles_asignados = relationship("UsuarioRol", back_populates="usuario", cascade="all, delete-orphan")


class Rol(Base):
    """
    Roles definidos dinámicamente en la base de datos.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)
    scope_tipo = Column(String(20), default="COLEGIO", nullable=False)  # "GLOBAL" o "COLEGIO"
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    permisos = relationship("RolPermiso", back_populates="rol", cascade="all, delete-orphan")


class Permiso(Base):
    """
    Permisos atómicos inmutables definidos en código y registrados en la base de datos.
    """
    __tablename__ = "permisos"
    __table_args__ = (UniqueConstraint("recurso", "accion", name="uq_recurso_accion"),)

    id = Column(Integer, primary_key=True, index=True)
    recurso = Column(String(50), nullable=False)  # e.g., "colegio", "alumno", "matricula"
    accion = Column(String(50), nullable=False)   # e.g., "crear", "leer", "editar", "eliminar", "aprobar"
    descripcion = Column(String(255), nullable=True)


class RolPermiso(Base):
    """
    Tabla intermedia que asocia un Rol con sus Permisos.
    """
    __tablename__ = "roles_permisos"

    id = Column(Integer, primary_key=True)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id", ondelete="CASCADE"), nullable=False)

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso")


class UsuarioRol(Base):
    """
    Vincula un usuario con un rol y define su ámbito geográfico/institucional (Scope).
    """
    __tablename__ = "usuarios_roles"
    __table_args__ = (
        UniqueConstraint("usuario_id", "rol_id", "colegio_id", name="uq_usuario_rol_colegio"),
    )

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="SET NULL"), nullable=True)  # NULL = Fundación completa (Global)

    usuario = relationship("Usuario", back_populates="roles_asignados")
    rol = relationship("Rol")
    colegio = relationship("Colegio", back_populates="usuarios_asociados")


class SesionActiva(Base):
    """
    Almacena los tokens de sesión activos de forma segura y persistente en la DB.
    """
    __tablename__ = "sesiones_activas"

    id = Column(Integer, primary_key=True)
    token = Column(String(64), unique=True, index=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    usuario = relationship("Usuario")

