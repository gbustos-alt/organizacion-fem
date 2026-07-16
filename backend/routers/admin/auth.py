from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import os
import urllib.parse
import httpx
from backend.core.templates import templates
from backend.core.database import get_db
from backend.models import Usuario, Rol, UsuarioRol
from backend.services.auth_service import (
    autenticar_usuario,
    crear_sesion,
    eliminar_sesion,
    obtener_usuario_de_sesion,
    get_password_hash
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


@router.get("/google/login")
async def google_login(request: Request):
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    
    # Si no están configuradas las credenciales, redirigir al simulador de desarrollo
    if not client_id or not redirect_uri:
        return RedirectResponse(url="/admin/auth/google/mock-login")
        
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        "response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote(redirect_uri)}&"
        "scope=openid%20email%20profile"
    )
    return RedirectResponse(url=google_auth_url)


@router.get("/google/mock-login", response_class=HTMLResponse)
async def google_mock_login_page(request: Request):
    # Solo permitir simulador si no están configuradas las credenciales
    if os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_REDIRECT_URI"):
        return RedirectResponse(url="/admin/auth/login")
        
    return templates.TemplateResponse(
        request=request,
        name="admin/google_mock_login.html",
        context={"error": None}
    )


@router.post("/google/mock-login", response_class=HTMLResponse)
async def google_mock_login_submit(
    request: Request,
    email: str = Form(...),
    nombre: str = Form(None)
):
    email = email.strip().lower()
    if not email.endswith("@fundacionfem.org"):
        return templates.TemplateResponse(
            request=request,
            name="admin/google_mock_login.html",
            context={"error": "La cuenta debe pertenecer estrictamente al dominio @fundacionfem.org"}
        )
        
    # Redirigir al callback simulando una respuesta exitosa
    username = nombre if nombre else email.split("@")[0]
    return RedirectResponse(
        url=f"/admin/auth/google/callback?email={email}&username={username}&mock=true",
        status_code=status.HTTP_303_SEE_OTHER
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    code: str = None,
    email: str = None,
    username: str = None,
    mock: bool = False,
    db: Session = Depends(get_db)
):
    # 1. Obtener email y datos del usuario
    if mock or (not code):
        # Modo simulación
        if not email or not email.endswith("@fundacionfem.org"):
            return RedirectResponse(url="/admin/auth/login?error=Acceso+denegado")
    else:
        # Modo real (Google OAuth)
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        
        async with httpx.AsyncClient() as client:
            # Intercambiar código por token de acceso
            token_res = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
                    "grant_type": "authorization_code"
                }
            )
            if token_res.status_code != 200:
                return RedirectResponse(url="/admin/auth/login?error=Fallo+de+autenticacion+con+Google")
                
            token_data = token_res.json()
            access_token = token_data.get("access_token")
            
            # Obtener datos de perfil
            userinfo_res = await client.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if userinfo_res.status_code != 200:
                return RedirectResponse(url="/admin/auth/login?error=Error+al+obtener+datos+de+usuario")
                
            user_info = userinfo_res.json()
            email = user_info.get("email", "").lower()
            username = user_info.get("given_name", email.split("@")[0])
            
            if not email.endswith("@fundacionfem.org"):
                return RedirectResponse(url="/admin/auth/login?error=Dominio+no+autorizado")

    # 2. Validar o registrar usuario en la base de datos
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        # Auto-registro para usuarios del dominio
        # Buscar el rol "Invitado" para asignarlo por defecto
        rol_invitado = db.query(Rol).filter(Rol.nombre == "Invitado").first()
        if not rol_invitado:
            # Fallback en caso de que la base de datos no esté sembrada
            rol_invitado = db.query(Rol).first()
            
        # Asegurar que el username no esté duplicado
        base_username = username
        counter = 1
        while db.query(Usuario).filter(Usuario.username == username).first():
            username = f"{base_username}{counter}"
            counter += 1
            
        user = Usuario(
            username=username,
            email=email,
            hashed_password=get_password_hash(os.urandom(16).hex()), # Contraseña aleatoria segura e inservible
            tipo="HUMANO",
            activo=True
        )
        db.add(user)
        db.flush()
        
        # Asignar rol de invitado
        if rol_invitado:
            rol_asoc = UsuarioRol(
                usuario_id=user.id,
                rol_id=rol_invitado.id,
                colegio_id=None
            )
            db.add(rol_asoc)
            
        db.commit()
        db.refresh(user)

    # 3. Validar estado del usuario
    if not user.activo:
        return RedirectResponse(url="/admin/auth/login?error=Usuario+inactivo")

    # 4. Establecer sesión
    token = crear_sesion(db, user.id)
    response = RedirectResponse(url="/admin/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="session_id",
        value=token,
        httponly=True,
        max_age=3600 * 12,
        samesite="lax",
        secure=False
    )
    return response
