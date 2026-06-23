import json
from sqlalchemy.orm import Session
from backend.models import RegistroAuditoria

def registrar_accion(
    db: Session,
    usuario_id: int,
    accion: str,
    recurso: str,
    recurso_id: int = None,
    colegio_id: int = None,
    valores_anteriores: dict = None,
    valores_nuevos: dict = None,
    ip_address: str = None
) -> RegistroAuditoria:
    """
    Crea un registro de auditoría en la base de datos de forma transaccional.
    Valores anteriores y nuevos se serializan a strings JSON para su posterior revisión.
    """
    val_ant_str = json.dumps(valores_anteriores, ensure_ascii=False) if valores_anteriores else None
    val_nuev_str = json.dumps(valores_nuevos, ensure_ascii=False) if valores_nuevos else None

    registro = RegistroAuditoria(
        usuario_id=usuario_id,
        colegio_id=colegio_id,
        accion=accion.upper(),
        recurso=recurso.lower(),
        recurso_id=recurso_id,
        valores_anteriores=val_ant_str,
        valores_nuevos=val_nuev_str,
        ip_address=ip_address
    )
    db.add(registro)
    db.commit()
    return registro
