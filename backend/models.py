import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from backend.core.database import Base

class Colegio(Base):
    __tablename__ = "colegios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    congregacion = Column(String(150), nullable=True)
    diocesis = Column(String(150), nullable=True)
    ubicacion = Column(String(200), nullable=True)
    provincia = Column(String(100), nullable=True)
    telefono = Column(String(50), nullable=True)
    web_url = Column(String(255), nullable=True)
    descripcion = Column(Text, nullable=True)
    imagen_url = Column(String(255), nullable=True)

class Noticia(Base):
    __tablename__ = "noticias"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    copete = Column(String(500), nullable=True)
    contenido = Column(Text, nullable=False)
    fecha_publicacion = Column(DateTime, default=datetime.datetime.utcnow)
    activa = Column(Boolean, default=True)

class MensajeContacto(Base):
    __tablename__ = "mensajes_contacto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefono = Column(String(50), nullable=True)
    mensaje = Column(Text, nullable=False)
    fecha_envio = Column(DateTime, default=datetime.datetime.utcnow)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
