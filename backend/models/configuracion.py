import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from backend.models.base import Base

class ConfiguracionLema(Base):
    """
    Define el Lema Anual y los objetivos institucionales de la Fundación FEM
    para un año particular, permitiendo su edición dinámica.
    """
    __tablename__ = "configuracion_lema"

    id = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, unique=True, nullable=False)
    lema_texto = Column(String(250), nullable=False)
    objetivos = Column(Text, nullable=True)  # Lista de objetivos separados por salto de línea
    imagen_lema_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)


class MemoriaAnual(Base):
    """
    Reportes anuales de rendición de cuentas institucionales en PDF para el público.
    """
    __tablename__ = "memorias_anuales"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    anio = Column(Integer, nullable=False)
    archivo_pdf_path = Column(String(255), nullable=False)  # Ruta al archivo guardado en el servidor
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class MaterialCapacitacion(Base):
    """
    Módulo de Capacitación Virtual (MOOC): recursos educativos y de inducción
    orientados a directores, educadores y representantes legales de la red.
    """
    __tablename__ = "materiales_capacitacion"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    categoria = Column(String(100), nullable=False)  # "Pastoral", "Gestión", "Pedagogía", "Inducción"
    archivo_url = Column(String(255), nullable=True)  # PDF u otro material de lectura
    video_url = Column(String(255), nullable=True)  # Link a video educativo (YouTube/Vimeo)
    activo = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
