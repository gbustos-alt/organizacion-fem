import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.models.base import Base

class AuditoriaIncorporacion(Base):
    """
    Representa el proceso de auditoría y seguimiento para la incorporación de un colegio
    candidato a la red de la Fundación FEM (Seguimiento y Elaboración).
    """
    __tablename__ = "auditorias_incorporacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    congregacion = Column(String(150), nullable=True)
    diocesis = Column(String(150), nullable=True)
    localidad = Column(String(150), nullable=True)
    provincia = Column(String(100), nullable=True)
    drive_folder_url = Column(String(255), nullable=True)
    estado = Column(String(20), default="PENDIENTE", nullable=False)  # PENDIENTE, EN_PROCESO, APROBADA, RECHAZADA

    # Área Pedagógica
    estado_pedagogica = Column(String(20), default="PENDIENTE", nullable=False)  # PENDIENTE, EN_PROCESO, COMPLETADO, OBSERVADO
    obs_pedagogica = Column(Text, nullable=True)

    # Área Pastoral
    estado_pastoral = Column(String(20), default="PENDIENTE", nullable=False)
    obs_pastoral = Column(Text, nullable=True)

    # Área Económica
    estado_economica = Column(String(20), default="PENDIENTE", nullable=False)
    obs_economica = Column(Text, nullable=True)

    # Área Legal
    estado_legal = Column(String(20), default="PENDIENTE", nullable=False)
    obs_legal = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
