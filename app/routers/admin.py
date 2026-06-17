from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """
    Ruta placeholder para el panel de administración interno.
    """
    return templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={"active_page": "admin"}
    )
