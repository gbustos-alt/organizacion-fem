import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models import Noticia, Actividad, MaterialReflexion, ConfiguracionLema, QuienesSomos, Usuario
from backend.services.rbac_service import RequerirPermiso, obtener_usuario_actual
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/api/v1", tags=["api-v1"])

def api_response(success: bool, data: Any = None, message: str = "", status_code: int = 200) -> JSONResponse:
    """
    Respuesta JSON estandarizada para la API REST.
    Estructura: { "success": true, "data": ..., "message": "..." }
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "data": data,
            "message": message
        }
    )

# --- Schemas Pydantic ---
class NovedadCreateUpdate(BaseModel):
    titulo: str
    copete: Optional[str] = None
    contenido: str
    imagen_url: Optional[str] = None
    activa: bool = True

class ActividadCreateUpdate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    lugar: Optional[str] = None
    fecha_inicio: Optional[str] = None
    adjunto_url: Optional[str] = None
    activa: bool = True

class ReflexionCreateUpdate(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    categoria: Optional[str] = "General"
    archivo_url: Optional[str] = None
    activo: bool = True

class ConfigHomeUpdate(BaseModel):
    lema_texto: Optional[str] = None
    objetivos: Optional[str] = None
    quienes_titulo: Optional[str] = None
    quienes_descripcion: Optional[str] = None


# ==========================================
# 1. NOVEDADES (/api/v1/novedades)
# ==========================================
@router.get("/novedades")
async def listar_novedades_api(
    solo_activas: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Noticia)
    if solo_activas:
        query = query.filter(Noticia.activa == True)
    novedades = query.order_by(Noticia.fecha_publicacion.desc()).all()
    
    data = [
        {
            "id": n.id,
            "titulo": n.titulo,
            "copete": n.copete,
            "contenido": n.contenido,
            "imagen_url": n.imagen_url,
            "activa": n.activa,
            "fecha_publicacion": n.fecha_publicacion.isoformat() if n.fecha_publicacion else None
        }
        for n in novedades
    ]
    return api_response(success=True, data=data, message="Novedades obtenidas exitosamente")

@router.post("/novedades")
async def crear_novedad_api(
    payload: NovedadCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("novedad", "crear"))
):
    nueva = Noticia(
        titulo=payload.titulo.strip(),
        copete=payload.copete.strip() if payload.copete else None,
        contenido=payload.contenido.strip(),
        imagen_url=payload.imagen_url,
        activa=payload.activa,
        fecha_publicacion=datetime.datetime.utcnow()
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="novedad",
        recurso_id=nueva.id,
        valores_nuevos={"titulo": nueva.titulo, "activa": nueva.activa}
    )

    data = {
        "id": nueva.id,
        "titulo": nueva.titulo,
        "copete": nueva.copete,
        "contenido": nueva.contenido,
        "imagen_url": nueva.imagen_url,
        "activa": nueva.activa,
        "fecha_publicacion": nueva.fecha_publicacion.isoformat() if nueva.fecha_publicacion else None
    }
    return api_response(success=True, data=data, message="Novedad creada exitosamente", status_code=21)

@router.put("/novedades/{novedad_id}")
async def editar_novedad_api(
    novedad_id: int,
    payload: NovedadCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("novedad", "editar"))
):
    novedad = db.query(Noticia).filter(Noticia.id == novedad_id).first()
    if not novedad:
        return api_response(success=False, message="Novedad no encontrada", status_code=404)

    novedad.titulo = payload.titulo.strip()
    novedad.copete = payload.copete.strip() if payload.copete else None
    novedad.contenido = payload.contenido.strip()
    novedad.imagen_url = payload.imagen_url
    novedad.activa = payload.activa
    db.commit()

    data = {
        "id": novedad.id,
        "titulo": novedad.titulo,
        "copete": novedad.copete,
        "contenido": novedad.contenido,
        "imagen_url": novedad.imagen_url,
        "activa": novedad.activa
    }
    return api_response(success=True, data=data, message="Novedad actualizada exitosamente")

@router.delete("/novedades/{novedad_id}")
async def eliminar_novedad_api(
    novedad_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("novedad", "eliminar"))
):
    novedad = db.query(Noticia).filter(Noticia.id == novedad_id).first()
    if not novedad:
        return api_response(success=False, message="Novedad no encontrada", status_code=404)

    db.delete(novedad)
    db.commit()
    return api_response(success=True, data={"id": novedad_id}, message="Novedad eliminada exitosamente")


# ==========================================
# 2. ACTIVIDADES (/api/v1/actividades)
# ==========================================
@router.get("/actividades")
async def listar_actividades_api(
    solo_activas: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(Actividad)
    if solo_activas:
        query = query.filter(Actividad.activa == True)
    actividades = query.order_by(Actividad.fecha.asc()).all()

    data = [
        {
            "id": a.id,
            "titulo": a.titulo,
            "descripcion": a.descripcion,
            "lugar": a.lugar,
            "fecha": a.fecha.isoformat() if a.fecha else None,
            "destinatarios": a.destinatarios,
            "link_inscripcion": a.link_inscripcion,
            "activa": a.activa
        }
        for a in actividades
    ]
    return api_response(success=True, data=data, message="Actividades obtenidas exitosamente")

@router.post("/actividades")
async def crear_actividad_api(
    payload: ActividadCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("actividad", "crear"))
):
    fecha_dt = None
    if payload.fecha_inicio:
        try:
            fecha_dt = datetime.datetime.fromisoformat(payload.fecha_inicio)
        except Exception:
            pass

    nueva = Actividad(
        titulo=payload.titulo.strip(),
        descripcion=payload.descripcion.strip() if payload.descripcion else "",
        lugar=payload.lugar.strip() if payload.lugar else "Virtual",
        fecha=fecha_dt or datetime.datetime.utcnow(),
        activa=payload.activa
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    data = {
        "id": nueva.id,
        "titulo": nueva.titulo,
        "descripcion": nueva.descripcion,
        "lugar": nueva.lugar,
        "fecha": nueva.fecha.isoformat() if nueva.fecha else None,
        "activa": nueva.activa
    }
    return api_response(success=True, data=data, message="Actividad creada exitosamente", status_code=201)

@router.put("/actividades/{actividad_id}")
async def editar_actividad_api(
    actividad_id: int,
    payload: ActividadCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("actividad", "editar"))
):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        return api_response(success=False, message="Actividad no encontrada", status_code=404)

    actividad.titulo = payload.titulo.strip()
    actividad.descripcion = payload.descripcion.strip() if payload.descripcion else ""
    actividad.lugar = payload.lugar.strip() if payload.lugar else "Virtual"
    actividad.activa = payload.activa
    if payload.fecha_inicio:
        try:
            actividad.fecha = datetime.datetime.fromisoformat(payload.fecha_inicio)
        except Exception:
            pass

    db.commit()
    data = {
        "id": actividad.id,
        "titulo": actividad.titulo,
        "descripcion": actividad.descripcion,
        "lugar": actividad.lugar,
        "activa": actividad.activa
    }
    return api_response(success=True, data=data, message="Actividad actualizada exitosamente")

@router.delete("/actividades/{actividad_id}")
async def eliminar_actividad_api(
    actividad_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("actividad", "eliminar"))
):
    actividad = db.query(Actividad).filter(Actividad.id == actividad_id).first()
    if not actividad:
        return api_response(success=False, message="Actividad no encontrada", status_code=404)

    db.delete(actividad)
    db.commit()
    return api_response(success=True, data={"id": actividad_id}, message="Actividad eliminada exitosamente")


# ==========================================
# 3. REFLEXIONES (/api/v1/reflexiones)
# ==========================================
@router.get("/reflexiones")
async def listar_reflexiones_api(
    solo_activos: bool = True,
    db: Session = Depends(get_db)
):
    query = db.query(MaterialReflexion)
    if solo_activos:
        query = query.filter(MaterialReflexion.activo == True)
    materiales = query.order_by(MaterialReflexion.fecha_publicacion.desc()).all()

    data = [
        {
            "id": m.id,
            "titulo": m.titulo,
            "autor": m.autor,
            "categoria": m.categoria,
            "contenido": m.contenido,
            "archivo_url": m.archivo_url,
            "activo": m.activo,
            "fecha_publicacion": m.fecha_publicacion.isoformat() if m.fecha_publicacion else None
        }
        for m in materiales
    ]
    return api_response(success=True, data=data, message="Materiales de reflexión obtenidos exitosamente")

@router.post("/reflexiones")
async def crear_reflexion_api(
    payload: ReflexionCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("material_reflexion", "crear"))
):
    nuevo = MaterialReflexion(
        titulo=payload.titulo.strip(),
        contenido=payload.descripcion.strip() if payload.descripcion else None,
        categoria=payload.categoria or "General",
        archivo_url=payload.archivo_url,
        activo=payload.activo,
        fecha_publicacion=datetime.datetime.utcnow()
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    data = {
        "id": nuevo.id,
        "titulo": nuevo.titulo,
        "contenido": nuevo.contenido,
        "categoria": nuevo.categoria,
        "archivo_url": nuevo.archivo_url,
        "activo": nuevo.activo
    }
    return api_response(success=True, data=data, message="Material de reflexión creado exitosamente", status_code=201)

@router.put("/reflexiones/{material_id}")
async def editar_reflexion_api(
    material_id: int,
    payload: ReflexionCreateUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("material_reflexion", "editar"))
):
    material = db.query(MaterialReflexion).filter(MaterialReflexion.id == material_id).first()
    if not material:
        return api_response(success=False, message="Material no encontrado", status_code=404)

    material.titulo = payload.titulo.strip()
    material.contenido = payload.descripcion.strip() if payload.descripcion else None
    material.categoria = payload.categoria or "General"
    material.archivo_url = payload.archivo_url
    material.activo = payload.activo
    db.commit()

    data = {
        "id": material.id,
        "titulo": material.titulo,
        "contenido": material.contenido,
        "categoria": material.categoria,
        "activo": material.activo
    }
    return api_response(success=True, data=data, message="Material actualizado exitosamente")


@router.delete("/reflexiones/{material_id}")
async def eliminar_reflexion_api(
    material_id: int,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("material_reflexion", "eliminar"))
):
    material = db.query(MaterialReflexion).filter(MaterialReflexion.id == material_id).first()
    if not material:
        return api_response(success=False, message="Material no encontrado", status_code=404)

    db.delete(material)
    db.commit()
    return api_response(success=True, data={"id": material_id}, message="Material eliminado exitosamente")


# ==========================================
# 4. CONFIG HOME (/api/v1/config/home)
# ==========================================
@router.get("/config/home")
async def obtener_config_home_api(db: Session = Depends(get_db)):
    lema = db.query(ConfiguracionLema).filter(ConfiguracionLema.anio == 2026).first()
    quienes = db.query(QuienesSomos).first()

    data = {
        "lema": {
            "anio": lema.anio if lema else 2026,
            "lema_texto": lema.lema_texto if lema else "Caminando juntos en la Educación y la Misión",
            "objetivos": lema.objetivos if lema else ""
        },
        "quienes_somos": {
            "titulo": quienes.titulo if quienes else "Qué Hacemos",
            "descripcion": quienes.descripcion if quienes else "",
            "imagen_url": quienes.imagen_url if quienes else "/static/img/fotos prueba/escuela.jpeg"
        }
    }
    return api_response(success=True, data=data, message="Configuración de la Home obtenida exitosamente")

@router.put("/config/home")
async def actualizar_config_home_api(
    payload: ConfigHomeUpdate,
    db: Session = Depends(get_db),
    user: Usuario = Depends(RequerirPermiso("configuracion", "editar"))
):
    lema = db.query(ConfiguracionLema).filter(ConfiguracionLema.anio == 2026).first()
    if not lema:
        lema = ConfiguracionLema(anio=2026, lema_texto="", activo=True)
        db.add(lema)

    if payload.lema_texto is not None:
        lema.lema_texto = payload.lema_texto.strip()
    if payload.objetivos is not None:
        lema.objetivos = payload.objetivos.strip()

    quienes = db.query(QuienesSomos).first()
    if not quienes:
        quienes = QuienesSomos(titulo="Qué Hacemos", descripcion="", activo=True)
        db.add(quienes)

    if payload.quienes_titulo is not None:
        quienes.titulo = payload.quienes_titulo.strip()
    if payload.quienes_descripcion is not None:
        quienes.descripcion = payload.quienes_descripcion.strip()

    db.commit()
    
    data = {
        "lema_texto": lema.lema_texto,
        "objetivos": lema.objetivos,
        "quienes_titulo": quienes.titulo,
        "quienes_descripcion": quienes.descripcion
    }
    return api_response(success=True, data=data, message="Configuración de la Home actualizada exitosamente")
