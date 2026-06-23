import os
import json
from sqlalchemy.orm import Session
from backend.models import Rol, Permiso, RolPermiso

def sincronizar_roles_y_permisos(db: Session, seed_filepath: str = None) -> dict:
    """
    Sincroniza permisos y roles de la base de datos a partir del archivo JSON semilla.
    Es una operación idempotente (evita duplicar registros).
    """
    if not seed_filepath:
        # Ruta por defecto
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        seed_filepath = os.path.join(base_dir, "backend", "core", "role_seed.json")

    if not os.path.exists(seed_filepath):
        raise FileNotFoundError(f"Archivo semilla no encontrado en: {seed_filepath}")

    with open(seed_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    resultados = {
        "permisos_creados": 0,
        "roles_creados": 0,
        "roles_actualizados": 0,
    }

    # 1. Asegurar el permiso comodín global
    comodin_permiso = db.query(Permiso).filter(
        Permiso.recurso == "*",
        Permiso.accion == "*"
    ).first()
    if not comodin_permiso:
        comodin_permiso = Permiso(
            recurso="*",
            accion="*",
            descripcion="Permiso superusuario absoluto"
        )
        db.add(comodin_permiso)
        db.flush()
        resultados["permisos_creados"] += 1

    # 2. Sincronizar permisos del sistema
    for item in data.get("permisos_sistema", []):
        recurso = item.get("recurso")
        acciones = item.get("acciones", [])
        descripcion = item.get("descripcion", "")

        for accion in acciones:
            permiso_db = db.query(Permiso).filter(
                Permiso.recurso == recurso,
                Permiso.accion == accion
            ).first()

            if not permiso_db:
                permiso_db = Permiso(
                    recurso=recurso,
                    accion=accion,
                    descripcion=f"{descripcion} - {accion.capitalize()}"
                )
                db.add(permiso_db)
                resultados["permisos_creados"] += 1

    db.flush()

    # 3. Sincronizar Roles y sus asociaciones
    for item in data.get("roles", []):
        nombre = item.get("nombre")
        descripcion = item.get("descripcion")
        scope_tipo = item.get("scope_tipo", "COLEGIO")
        permisos_seed = item.get("permisos", [])

        rol_db = db.query(Rol).filter(Rol.nombre == nombre).first()
        if not rol_db:
            rol_db = Rol(
                nombre=nombre,
                descripcion=descripcion,
                scope_tipo=scope_tipo
            )
            db.add(rol_db)
            db.flush()
            resultados["roles_creados"] += 1
        else:
            rol_db.descripcion = descripcion
            rol_db.scope_tipo = scope_tipo
            resultados["roles_actualizados"] += 1

        # Limpiar asociaciones viejas de permisos de este rol para re-vincularlas
        db.query(RolPermiso).filter(RolPermiso.rol_id == rol_db.id).delete()
        db.flush()

        # Vincular permisos definidos
        for p_seed in permisos_seed:
            rec_seed = p_seed.get("recurso")
            acc_seed = p_seed.get("acciones", [])

            # Si es comodín global, le asignamos el permiso comodín "*"
            if rec_seed == "*" and "*" in acc_seed:
                asoc = RolPermiso(rol_id=rol_db.id, permiso_id=comodin_permiso.id)
                db.add(asoc)
            else:
                # Buscar permisos coincidentes en la base de datos
                # E.g., para recurso "alumno" y acciones ["crear", "leer"]
                for acc in acc_seed:
                    p_db = db.query(Permiso).filter(
                        Permiso.recurso == rec_seed,
                        Permiso.accion == acc
                    ).first()
                    if p_db:
                        asoc = RolPermiso(rol_id=rol_db.id, permiso_id=p_db.id)
                        db.add(asoc)

    db.commit()
    return resultados
