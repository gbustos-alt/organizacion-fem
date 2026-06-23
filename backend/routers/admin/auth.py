from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from backend.core.templates import templates
from backend.core.database import get_db
from backend.services.auth_service import (
    autenticar_usuario,
    crear_sesion,
    eliminar_sesion,
    obtener_usuario_de_sesion
)

router = APIRouter(prefix="/auth", tags=["admin-auth"])

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, db: Session = Depends(get_db)):
    """
    Muestra la página de login si el usuario no tiene una sesión activa.
    Si ya está logueado, lo redirige al dashboard.
    """
    session_token = request.cookies.get("session_id")
    if session_token:
        user = obtener_usuario_de_sesion(db, session_token)
        if user and user.activo:
            return RedirectResponse(url="/admin/", status_code=status.HTTP_303_SEE_OTHER)
        
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={"error": None}
    )

@router.post("/login", response_class=HTMLResponse)
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Procesa el envío del formulario de login y establece la sesión.
    """
    user = autenticar_usuario(db, username, password)
    if not user:
        return templates.TemplateResponse(
            request=request,
            name="admin/login.html",
            context={"error": "Usuario o contraseña incorrectos.", "username": username},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    # Crear la sesión en la base de datos
    token = crear_sesion(db, user.id)
    
    # Establecer la cookie en la respuesta y redirigir
    response = RedirectResponse(url="/admin/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="session_id",
        value=token,
        httponly=True,
        max_age=3600 * 12,  # 12 horas
        samesite="lax",
        secure=False  # Cambiar a True en producción con HTTPS
    )
    return response

@router.get("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """
    Cierra la sesión del usuario y lo redirige al login.
    """
    session_token = request.cookies.get("session_id")
    if session_token:
        eliminar_sesion(db, session_token)
        
    response = RedirectResponse(url="/admin/auth/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")
    return response
