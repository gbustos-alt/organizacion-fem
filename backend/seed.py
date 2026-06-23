import hashlib
from backend.core.database import SessionLocal, Base, engine
from backend.models import Colegio, Noticia, Usuario, Rol, UsuarioRol
from backend.services.import_service import sincronizar_roles_y_permisos

def get_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def seed_db():
    # Asegurar tablas recreadas con campos nuevos
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Colegios Oficiales de la Fundación
    colegios = [
        # CABA
        Colegio(
            nombre="Instituto Santa Ana y San Joaquín",
            congregacion="Congregación Hijas de Santa Ana",
            ubicacion="Olazábal 1440, Belgrano",
            provincia="CABA",
            telefono="011 4784 7650",
            web_url="http://www.santaanaysanjoaquin.edu.ar"
        ),
        Colegio(
            nombre="Instituto Superior Santa Ana",
            congregacion="Congregación Hijas de Santa Ana",
            ubicacion="Av. del Libertador 6155, Belgrano",
            provincia="CABA",
            telefono="011 4784 6795",
            web_url="http://www.santaanaysanjoaquin.edu.ar"
        ),
        Colegio(
            nombre="Instituto Plácido Marín",
            congregacion="Congregación Esclavas del Divino Corazón",
            ubicacion="Larrazábal 1551, Mataderos",
            provincia="CABA",
            telefono="011 4635 0115",
            web_url="http://www.placidomarin.edu.ar"
        ),
        Colegio(
            nombre="Instituto San Pío X",
            congregacion="Hermandad Sacerdotes Operarios Diocesanos",
            ubicacion="Basualdo 780, Mataderos",
            provincia="CABA",
            telefono="011 4635 1710",
            web_url="http://www.institutosanpiox.edu.ar"
        ),
        # PBA
        Colegio(
            nombre="Instituto Dolores Rodríguez Sopeña",
            congregacion="Congregación Catequistas de Dolores Sopeña",
            ubicacion="España 620, Avellaneda",
            provincia="Provincia de Buenos Aires",
            telefono="011 4222 6814"
        ),
        Colegio(
            nombre="Colegio Cardenal Spínola",
            congregacion="Congregación Esclavas del Divino Corazón",
            ubicacion="Maestro Santana 349, San Isidro",
            provincia="Provincia de Buenos Aires",
            telefono="011 4723 4394",
            web_url="http://www.cardenalspinola.com.ar"
        ),
        Colegio(
            nombre="Colegio Sagrada Familia (Zárate)",
            congregacion="Congregación Hijas de la Cruz",
            ubicacion="Félix Pagola 125, Zárate",
            provincia="Provincia de Buenos Aires",
            telefono="03487 422423",
            web_url="http://www.csfamilia.com.ar"
        ),
        Colegio(
            nombre="I.S.F.D. Sagrada Familia",
            congregacion="Congregación Hijas de la Cruz",
            ubicacion="Félix Pagola 125, Zárate",
            provincia="Provincia de Buenos Aires",
            web_url="mailto:nivelsuperior@csfamilia.com.ar"
        ),
        Colegio(
            nombre="Colegio Sagrada Familia e Inst. Hijas de la Cruz",
            congregacion="Congregación Hijas de la Cruz",
            ubicacion="Calle 15 (entre 51 y 53) Nº 961, La Plata",
            provincia="Provincia de Buenos Aires",
            telefono="0221 4212231",
            web_url="http://www.csfamilialp.com.ar"
        ),
        Colegio(
            nombre="Instituto Nuestra Señora del Carmen",
            congregacion="Orden Carmelita",
            ubicacion="Fonrouge 855, Lomas de Zamora",
            provincia="Provincia de Buenos Aires",
            telefono="WhatsApp: +54 9 11 4243 9089",
            web_url="http://www.inscarmen.edu.ar"
        ),
        Colegio(
            nombre="Colegio San Juan de la Cruz",
            congregacion="Orden Carmelita",
            ubicacion="General Pintos 1450, Banfield",
            provincia="Provincia de Buenos Aires",
            telefono="011 4245 0614",
            web_url="http://www.sanjuandelacruz.edu.ar"
        ),
        # Presencia Federal
        Colegio(
            nombre="Colegio Sagrado Corazón (Jujuy)",
            congregacion="Congregación Esclavas del Divino Corazón",
            ubicacion="Av. Luciano Catalano 198, Palpalá, Jujuy",
            provincia="Presencia Federal",
            telefono="0388 427 0198"
        ),
        Colegio(
            nombre="Instituto Corazón de Jesús (Santa Fe)",
            congregacion="Congregación Esclavas del Divino Corazón",
            ubicacion="Rivadavia 713, San Carlos Centro, Santa Fe",
            provincia="Presencia Federal",
            telefono="03404 42 0055",
            web_url="https://instagram.com/corazondejesus_sc"
        ),
        Colegio(
            nombre="Colegio e Instituto Montserrat (Tucumán)",
            congregacion="Hermandad Sacerdotes Operarios Diocesanos",
            ubicacion="Colombia 2937, San Miguel de Tucumán, Tucumán",
            provincia="Presencia Federal",
            telefono="0381 254 7338",
            web_url="http://www.colegio-e-instituto-montserrat.com"
        ),
        Colegio(
            nombre="Colegio Nuestra Señora de la Compasión (Mendoza)",
            congregacion="Compasionistas",
            ubicacion="Soberanía Nacional y Congreso de Tucumán, Palmira, Mendoza",
            provincia="Presencia Federal",
            telefono="0263 4461778"
        )
    ]
    db.add_all(colegios)
    
    # 2. Agregar Noticias
    noticias = [
        Noticia(
            titulo="Encuentro de Directivos 2026",
            copete="Se celebró el primer encuentro inter-carismático para coordinar los ejes del nuevo ciclo lectivo.",
            contenido="Con la presencia de delegaciones de más de veinte colegios, compartimos jornadas de reflexión, oración y planificación de la gestión eclesial y educativa."
        ),
        Noticia(
            titulo="Campaña Solidaria de Invierno",
            copete="Las comunidades de la red de colegios inician colecta para comedores comunitarios.",
            contenido="Como parte de nuestra misión de fraternidad y servicio eclesial, invitamos a sumarse a la colecta anual de abrigo y alimentos no perecederos."
        )
    ]
    db.add_all(noticias)
    
    # 3. Sincronizar Roles y Permisos desde archivo de configuración
    print("🔑 Sincronizando roles y permisos desde semilla...")
    sincronizar_roles_y_permisos(db)

    # 4. Obtener roles creados
    rol_admin = db.query(Rol).filter(Rol.nombre == "Administrador General").first()
    rol_director = db.query(Rol).filter(Rol.nombre == "Director de Colegio").first()

    # 5. Agregar Usuario Administrador (Global)
    admin_user = Usuario(
        username="admin",
        email="admin@fundacionfem.org",
        hashed_password=get_password_hash("admin123"),
        tipo="HUMANO",
        activo=True
    )
    db.add(admin_user)
    db.flush()

    # Asignar rol Administrador General (Global: colegio_id=None)
    admin_rol_asoc = UsuarioRol(
        usuario_id=admin_user.id,
        rol_id=rol_admin.id,
        colegio_id=None
    )
    db.add(admin_rol_asoc)

    # 6. Agregar Usuario Director (Limitado al primer colegio de la lista)
    primer_colegio = db.query(Colegio).first()
    director_user = Usuario(
        username="director",
        email="director@fundacionfem.org",
        hashed_password=get_password_hash("director123"),
        tipo="HUMANO",
        activo=True
    )
    db.add(director_user)
    db.flush()

    if primer_colegio:
        # Asignar rol Director de Colegio (Local: colegio_id del primer colegio)
        director_rol_asoc = UsuarioRol(
            usuario_id=director_user.id,
            rol_id=rol_director.id,
            colegio_id=primer_colegio.id
        )
        db.add(director_rol_asoc)
        print(f"👤 Creado usuario director asignado a: {primer_colegio.nombre}")

    # 7. Agregar Agente Automatizado (Global)
    agente_user = Usuario(
        username="agente_auditor",
        email="agente@fundacionfem.org",
        hashed_password=get_password_hash("agente123"),
        tipo="AGENTE",
        activo=True
    )
    db.add(agente_user)
    db.flush()

    agente_rol_asoc = UsuarioRol(
        usuario_id=agente_user.id,
        rol_id=rol_admin.id,
        colegio_id=None
    )
    db.add(agente_rol_asoc)

    db.commit()
    db.close()
    print("✅ Base de datos poblada y RBAC inicial configurado exitosamente.")

if __name__ == "__main__":
    seed_db()
