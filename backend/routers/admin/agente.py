from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.rbac_service import obtener_usuario_actual
from backend.services.agente_service import procesar_consulta_agente

router = APIRouter(prefix="/agente", tags=["admin-agente"])

@router.get("/", response_class=HTMLResponse)
async def panel_agente(
    request: Request,
    user = Depends(obtener_usuario_actual)
):
    """
    Renderiza la vista principal del Asistente de Gestión (Agente FEM).
    """
    return templates.TemplateResponse(
        request=request,
        name="admin/agente.html",
        context={"user": user, "active_page": "agente"}
    )

@router.post("/consultar", response_class=JSONResponse)
async def consultar_agente(
    request: Request,
    query: str = Form(...),
    db: Session = Depends(get_db),
    user = Depends(obtener_usuario_actual)
):
    """
    Procesa una consulta del Asistente y retorna la respuesta en formato JSON
    para posibilitar una experiencia interactiva sin refrescar la página.
    """
    resultado = procesar_consulta_agente(db, query)
    return JSONResponse(content=resultado)
