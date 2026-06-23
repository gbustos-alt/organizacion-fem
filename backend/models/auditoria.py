import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base

class RegistroAuditoria(Base):
    """
    Log de transacciones para auditoría y seguridad.
    """
    __tablename__ = "registros_auditoria"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="SET NULL"), nullable=True)  # Scope escolar
    accion = Column(String(20), nullable=False)      # "CREAR", "MODIFICAR", "ELIMINAR", "APROBAR"
    recurso = Column(String(50), nullable=False)     # "alumno", "matricula", "colegio"
    recurso_id = Column(Integer, nullable=True)
    valores_anteriores = Column(String, nullable=True)  # JSON String
    valores_nuevos = Column(String, nullable=True)      # JSON String
    ip_address = Column(String(45), nullable=True)

    usuario = relationship("Usuario")
    colegio = relationship("Colegio")
