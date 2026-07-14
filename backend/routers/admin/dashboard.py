from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import obtener_usuario_actual
from backend.models import Colegio, Noticia, Actividad, MaterialReflexion, Usuario, SesionActiva

router = APIRouter(tags=["admin-dashboard"])

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(obtener_usuario_actual)
):
    """
    Ruta para la página principal de la intranet. Muestra métricas institucionales reales.
    """
    colegios_count = db.query(Colegio).count()
    novedades_count = db.query(Noticia).count()
    actividades_count = db.query(Actividad).count()
    materiales_count = db.query(MaterialReflexion).count()
    usuarios_activos = db.query(SesionActiva).count()
    
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "user": user,
            "active_page": "dashboard",
            "colegios_count": colegios_count,
            "novedades_count": novedades_count,
            "actividades_count": actividades_count,
            "materiales_count": materiales_count,
            "usuarios_activos": usuarios_activos
        }
    )
