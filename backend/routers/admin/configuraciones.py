import os
import shutil
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import RequerirPermiso
from backend.models import ConfiguracionLema, MemoriaAnual, MaterialCapacitacion
from backend.services.audit_service import registrar_accion

router = APIRouter(prefix="/configuraciones", tags=["admin-configuraciones"])

# Directorio físico donde guardaremos los archivos en el servidor
UPLOAD_DIR = os.path.join("frontend", "uploads")

def asegurar_directorio_cargas():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

@router.get("/", response_class=HTMLResponse)
async def dashboard_configuraciones(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("configuracion", "leer"))
):
    # Obtener el lema del año actual (ej: 2026) o crear uno por defecto si no existe
    anio_actual = datetime_anio_actual = 2026
    lema = db.query(ConfiguracionLema).filter(ConfiguracionLema.anio == anio_actual).first()
    if not lema:
        lema = ConfiguracionLema(
            anio=anio_actual,
            lema_texto="Escriba aquí el lema anual",
            objetivos="Objetivo 1\nObjetivo 2",
            activo=True
        )
        db.add(lema)
        db.commit()
        db.refresh(lema)
        
    memorias = db.query(MemoriaAnual).order_by(MemoriaAnual.anio.desc()).all()
    materiales_mooc = db.query(MaterialCapacitacion).order_by(MaterialCapacitacion.created_at.desc()).all()
    
    return templates.TemplateResponse(
        request=request,
        name="admin/configuraciones/dashboard.html",
        context={
            "user": user,
            "active_page": "configuraciones",
            "lema": lema,
            "memorias": memorias,
            "materiales_mooc": materiales_mooc
        }
    )

@router.post("/lema/editar", response_class=HTMLResponse)
async def editar_lema_submit(
    request: Request,
    lema_texto: str = Form(...),
    objetivos: str = Form(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("configuracion", "editar"))
):
    anio_actual = 2026
    lema = db.query(ConfiguracionLema).filter(ConfiguracionLema.anio == anio_actual).first()
    if not lema:
        raise HTTPException(status_code=404, detail="Configuración de lema no encontrada")
        
    valores_anteriores = {
        "lema_texto": lema.lema_texto,
        "objetivos": lema.objetivos
    }
    
    lema.lema_texto = lema_texto.strip()
    lema.objetivos = objetivos.strip() if objetivos else None
    
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="editar",
        recurso="configuracion_lema",
        recurso_id=lema.id,
        valores_anteriores=valores_anteriores,
        valores_nuevos={"lema_texto": lema.lema_texto, "objetivos": lema.objetivos}
    )
    
    db.commit()
    return RedirectResponse(url="/admin/configuraciones/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/memorias/crear", response_class=HTMLResponse)
async def crear_memoria_submit(
    request: Request,
    titulo: str = Form(...),
    anio: int = Form(...),
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("configuracion", "editar"))
):
    asegurar_directorio_cargas()
    
    # Validar extensión de archivo
    if not archivo.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Formato inválido: Solo se permiten archivos PDF.")
        
    # Guardar archivo físicamente
    nombre_archivo = f"memoria_{anio}_{int(os.urandom(4).hex(), 16)}.pdf"
    ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)
    
    with open(ruta_archivo, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)
        
    archivo_url = f"/static/uploads/{nombre_archivo}"
    
    nueva_memoria = MemoriaAnual(
        titulo=titulo.strip(),
        anio=anio,
        archivo_pdf_path=archivo_url,
        activo=True
    )
    db.add(nueva_memoria)
    db.flush()
    
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="memoria_anual",
        recurso_id=nueva_memoria.id,
        valores_nuevos={"titulo": nueva_memoria.titulo, "anio": anio, "archivo_pdf_path": archivo_url}
    )
    
    db.commit()
    return RedirectResponse(url="/admin/configuraciones/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/memorias/eliminar/{memoria_id}", response_class=HTMLResponse)
async def eliminar_memoria(
    memoria_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("configuracion", "editar"))
):
    memoria = db.query(MemoriaAnual).filter(MemoriaAnual.id == memoria_id).first()
    if not memoria:
        raise HTTPException(status_code=404, detail="Memoria no encontrada")
        
    # Intentar eliminar el archivo físico del disco si existe
    nombre_archivo = memoria.archivo_pdf_path.split("/")[-1]
    ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)
    if os.path.exists(ruta_archivo):
        try:
            os.remove(ruta_archivo)
        except Exception:
            pass
            
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="eliminar",
        recurso="memoria_anual",
        recurso_id=memoria.id,
        valores_anteriores={"titulo": memoria.titulo, "archivo_pdf_path": memoria.archivo_pdf_path}
    )
    
    db.delete(memoria)
    db.commit()
    return RedirectResponse(url="/admin/configuraciones/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/capacitacion/crear", response_class=HTMLResponse)
async def crear_capacitacion_submit(
    request: Request,
    titulo: str = Form(...),
    descripcion: str = Form(None),
    categoria: str = Form(...),
    video_url: str = Form(None),
    archivo: UploadFile = File(None),
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("capacitacion", "crear"))
):
    archivo_url = None
    if archivo and archivo.filename:
        asegurar_directorio_cargas()
        # Limpiar nombre
        ext = os.path.splitext(archivo.filename)[1]
        nombre_archivo = f"capacitacion_{int(os.urandom(4).hex(), 16)}{ext}"
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)
        
        with open(ruta_archivo, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
            
        archivo_url = f"/static/uploads/{nombre_archivo}"
        
    nuevo_material = MaterialCapacitacion(
        titulo=titulo.strip(),
        descripcion=descripcion.strip() if descripcion else None,
        categoria=categoria,
        archivo_url=archivo_url,
        video_url=video_url.strip() if video_url else None,
        activo=True
    )
    
    db.add(nuevo_material)
    db.flush()
    
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="crear",
        recurso="material_capacitacion",
        recurso_id=nuevo_material.id,
        valores_nuevos={"titulo": nuevo_material.titulo, "categoria": categoria, "archivo_url": archivo_url}
    )
    
    db.commit()
    return RedirectResponse(url="/admin/configuraciones/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/capacitacion/eliminar/{material_id}", response_class=HTMLResponse)
async def eliminar_capacitacion(
    material_id: int,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("capacitacion", "eliminar"))
):
    material = db.query(MaterialCapacitacion).filter(MaterialCapacitacion.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
        
    # Eliminar archivo del disco si existe
    if material.archivo_url:
        nombre_archivo = material.archivo_url.split("/")[-1]
        ruta_archivo = os.path.join(UPLOAD_DIR, nombre_archivo)
        if os.path.exists(ruta_archivo):
            try:
                os.remove(ruta_archivo)
            except Exception:
                pass
                
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="eliminar",
        recurso="material_capacitacion",
        recurso_id=material.id,
        valores_anteriores={"titulo": material.titulo, "archivo_url": material.archivo_url}
    )
    
    db.delete(material)
    db.commit()
    return RedirectResponse(url="/admin/configuraciones/", status_code=status.HTTP_303_SEE_OTHER)
