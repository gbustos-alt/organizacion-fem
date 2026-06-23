import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.models.base import Base

class Alumno(Base):
    """
    Estudiante perteneciente a un Colegio.
    """
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    documento = Column(String(20), unique=True, index=True, nullable=False)
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="RESTRICT"), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    colegio = relationship("Colegio")


class Matricula(Base):
    """
    Estado de inscripción anual de un alumno.
    """
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id", ondelete="RESTRICT"), nullable=False)
    ciclo_lectivo = Column(Integer, nullable=False)  # e.g., 2026
    estado = Column(String(20), default="PENDIENTE", nullable=False)  # "PENDIENTE", "APROBADA", "RECHAZADA"
    colegio_id = Column(Integer, ForeignKey("colegios.id", ondelete="RESTRICT"), nullable=False)
    fecha_solicitud = Column(DateTime, default=datetime.datetime.utcnow)

    alumno = relationship("Alumno")
    colegio = relationship("Colegio")
