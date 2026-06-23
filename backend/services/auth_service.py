import hashlib
import secrets
from sqlalchemy.orm import Session
from backend.models import Usuario, SesionActiva

def get_password_hash(password: str) -> str:
    """
    Genera el hash SHA-256 de una contraseña.
    Usa el mismo formato que backend/seed.py para consistencia.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica que la contraseña plana coincida con el hash almacenado.
    """
    return get_password_hash(plain_password) == hashed_password

def autenticar_usuario(db: Session, username: str, password: str) -> Usuario:
    """
    Busca un usuario por su nombre y valida la contraseña.
    Retorna el modelo de Usuario si es válido y activo, o None de lo contrario.
    """
    usuario = db.query(Usuario).filter(Usuario.username == username, Usuario.activo == True).first()
    if not usuario:
        return None
    if not verificar_password(password, usuario.hashed_password):
        return None
    return usuario

def crear_sesion(db: Session, usuario_id: int) -> str:
    """
    Genera un token de sesión seguro, lo registra en la base de datos y lo retorna.
    """
    token = secrets.token_hex(32)
    nueva_sesion = SesionActiva(token=token, usuario_id=usuario_id)
    db.add(nueva_sesion)
    db.commit()
    return token

def eliminar_sesion(db: Session, token: str) -> None:
    """
    Elimina un token de sesión activo de la base de datos.
    """
    db.query(SesionActiva).filter(SesionActiva.token == token).delete()
    db.commit()

def obtener_usuario_de_sesion(db: Session, token: str) -> Usuario:
    """
    Busca y retorna el usuario asociado al token de sesión si la sesión es válida.
    """
    sesion = db.query(SesionActiva).filter(SesionActiva.token == token).first()
    if not sesion:
        return None
    # Podemos verificar expiración aquí si agregamos expires_at
    return sesion.usuario
