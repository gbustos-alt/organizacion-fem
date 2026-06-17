from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.templates import templates

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Ruta para la página de inicio institucional.
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"active_page": "home"}
    )

@router.get("/nosotros", response_class=HTMLResponse)
async def nosotros(request: Request):
    """
    Ruta para la página 'Nosotros' de la institución.
    """
    return templates.TemplateResponse(
        request=request,
        name="nosotros.html",
        context={"active_page": "nosotros"}
    )
