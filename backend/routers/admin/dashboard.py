from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import obtener_usuario_actual
from backend.models import Colegio, Alumno, Matricula, Usuario, SesionActiva

router = APIRouter(tags=["admin-dashboard"])

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    db: Session = Depends(get_db),
    user: Usuario = Depends(obtener_usuario_actual)
):
    """
    Ruta para la página principal de la intranet. Muestra métricas rápidas reales e ingresos estimados.
    """
    colegios_count = db.query(Colegio).count()
    alumnos_count = db.query(Alumno).count()
    matriculas_count = db.query(Matricula).filter(Matricula.estado == "PENDIENTE").count()
    
    # Calcular ingresos estimados arancelarios basados en cuota promedio de $35,000 ARS
    ingresos_estimados = alumnos_count * 35000
    
    # Cantidad de sesiones activas reales en el sistema
    usuarios_activos = db.query(SesionActiva).count()
    
    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "user": user,
            "active_page": "dashboard",
            "colegios_count": colegios_count,
            "alumnos_count": alumnos_count,
            "matriculas_count": matriculas_count,
            "ingresos_estimados": ingresos_estimados,
            "usuarios_activos": usuarios_activos
        }
    )
