import hashlib
import datetime
from backend.core.database import SessionLocal, Base, engine
from backend.models import Colegio, Noticia, MaterialReflexion, Actividad, Usuario, Rol, UsuarioRol, AuditoriaIncorporacion, ConfiguracionLema, MemoriaAnual, MaterialCapacitacion
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
            titulo="Encuentro Federal de Equipos de Conducción",
            copete="Directivos de los colegios de nuestra red compartieron una jornada de trabajo, capacitación y oración presencial.",
            contenido="Directivos de los colegios de nuestra red y miembros de la junta directiva de FAERA compartieron una jornada de trabajo, capacitación y oración presencial, consolidando los pilares pedagógicos y administrativos de la gobernanza inter-carismática.",
            imagen_url="/static/img/fotos prueba/novedad_encuentro.png",
            fecha_publicacion=datetime.datetime(2026, 6, 28)
        ),
        Noticia(
            titulo="Proceso de Transición en el Colegio San José",
            copete="Sistematizamos la primera etapa del camino de acompañamiento institucional, enfocado en resguardar la identidad de las fundadoras.",
            contenido="Sistematizamos la primera etapa del camino de acompañamiento institucional, enfocado en resguardar la identidad de las Hermanas Fundadoras y proyectar su sustentabilidad a largo plazo.",
            imagen_url="/static/img/fotos prueba/novedad_transicion.png",
            fecha_publicacion=datetime.datetime(2026, 6, 15)
        ),
        Noticia(
            titulo="Taller de Sostenibilidad Administrativa",
            copete="Presentamos a los administradores de la red las nuevas herramientas de autodiagnóstico financiero.",
            contenido="Presentamos a los administradores de la red las nuevas herramientas de autodiagnóstico financiero para optimizar la toma de decisiones presupuestarias y de cuota.",
            imagen_url="/static/img/fotos prueba/novedad_sostenibilidad.png",
            fecha_publicacion=datetime.datetime(2026, 6, 2)
        )
    ]
    db.add_all(noticias)

    # 3. Agregar Materiales de Reflexión
    materiales = [
        MaterialReflexion(
            titulo="Cita Inspiradora Anual",
            autor="Fundación Educación y Misión & FAERA",
            categoria="Cita Inspiradora",
            contenido="La educación católica es un acto de amor y de esperanza que nos convoca a caminar juntos, resguardando nuestra historia y proyectando el futuro de nuestras comunidades.",
            activo=True
        ),
        MaterialReflexion(
            titulo="Recursos Pedagógicos Curriculares",
            autor="Junta Directiva FEM",
            categoria="Pedagógico",
            contenido="Herramientas y marcos curriculares para la planificación pedagógica de los niveles primario y secundario.",
            archivo_url="/static/docs/Puntos_Referencia_FEM_2026.pdf",
            imagen_url="/static/img/fotos prueba/escuela.jpeg",
            activo=True
        ),
        MaterialReflexion(
            titulo="Materiales para Catequesis y Pastoral Escolar",
            autor="Equipo Pastoral FEM",
            categoria="Pastoral",
            contenido="Fichas de trabajo y guías para celebraciones litúrgicas en tiempos de adviento y cuaresma.",
            link_url="https://www.youtube.com/watch?v=ejemplo-pastoral",
            imagen_url="/static/img/fotos prueba/ninos.jpeg",
            activo=True
        ),
        MaterialReflexion(
            titulo="Guías Docentes y Proyectos Colaborativos",
            autor="Asesoría Editorial FEM",
            categoria="Editorial",
            contenido="Guías orientativas para docentes sobre la integración de proyectos comunitarios intercolegiales.",
            imagen_url="/static/img/fotos prueba/library.jpeg",
            activo=True
        ),
        MaterialReflexion(
            titulo="Formación Continua para Directores",
            autor="Formadores Asociados FEM",
            categoria="Pedagógico",
            contenido="Módulos de capacitación y actualización académica para directores noveles en la red.",
            imagen_url="/static/img/fotos prueba/2016_10_26_ALTA_RESOLUCION_0163-scaled1.jpg",
            activo=True
        )
    ]
    db.add_all(materiales)

    # 4. Agregar Actividades
    actividades = [
        Actividad(
            titulo="Encuentro de Representantes Legales y Administradores",
            descripcion="Revisión de procesos económico-financieros, formación en marcos regulatorios y firma de acuerdos estratégicos.",
            fecha=datetime.datetime(2026, 8, 15, 9, 0),
            lugar="Sede Central FAERA (Lavalle 1527, CABA)",
            destinatarios="Representantes Legales y Administradores",
            link_inscripcion="https://forms.gle/ejemplo-inscripcion-rl",
            activa=True
        ),
        Actividad(
            titulo="Jornada Virtual de Pastoral Educativa",
            descripcion="Itinerarios orientados a retomar el sentido profundamente evangelizador de la tarea escolar escolar.",
            fecha=datetime.datetime(2026, 9, 10, 18, 0),
            lugar="Plataforma Virtual Zoom",
            destinatarios="Coordinadores de Pastoral y Docentes",
            link_inscripcion="https://zoom.us/j/ejemplo-pastoral-zoom",
            activa=True
        )
    ]
    db.add_all(actividades)
    
    # 5. Agregar Lema Anual
    lema = ConfiguracionLema(
        anio=2026,
        lema_texto="Caminando juntos en la Educación y la Misión",
        objetivos="Fortalecer los lazos de fraternidad eclesial en toda la red de colegios.\nConsolidar los equipos de gestión pedagógica pastoral.\nDigitalizar los procesos de auditoría administrativa y contable.",
        imagen_lema_url="/static/img/lema-fem-2026.png",
        activo=True
    )
    db.add(lema)

    # 6. Agregar Memorias Anuales
    memorias = [
        MemoriaAnual(titulo="Memoria Anual y Balance Social 2024", anio=2024, archivo_pdf_path="/static/uploads/memoria_2024.pdf", activo=True),
        MemoriaAnual(titulo="Memoria Anual e Informe de Gestión 2025", anio=2025, archivo_pdf_path="/static/uploads/memoria_2025.pdf", activo=True)
    ]
    db.add_all(memorias)

    # 7. Agregar Materiales de Capacitación
    capacitaciones = [
        MaterialCapacitacion(
            titulo="Inducción al Carisma de la Fundación FEM",
            descripcion="Curso introductorio sobre la historia, misión y valores de la Fundación FEM para nuevos docentes y directivos.",
            categoria="Inducción",
            archivo_url="/static/uploads/material_induccion_carisma.pdf",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ),
        MaterialCapacitacion(
            titulo="Guía de Administración y Rendición Contable Escolar",
            descripcion="Herramientas y plantillas para la gestión contable interna de los colegios asociados.",
            categoria="Gestión",
            archivo_url="/static/uploads/guia_gestion_contable.pdf"
        ),
        MaterialCapacitacion(
            titulo="El Rol del Director en el Acompañamiento Pastoral",
            descripcion="Estrategias prácticas para directores de colegios sobre cómo liderar la pastoral escolar.",
            categoria="Pastoral",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )
    ]
    db.add_all(capacitaciones)

    # 8. Agregar Escuelas Candidatas (Auditoría de Incorporación)
    candidatos = [
        AuditoriaIncorporacion(
            nombre="Col. María de Luján Sierra", congregacion="Hijas de la Cruz", localidad="La Plata", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo1",
            estado="EN_PROCESO", estado_pedagogica="COMPLETADO", estado_pastoral="EN_PROCESO", estado_economica="PENDIENTE", estado_legal="PENDIENTE",
            obs_pedagogica="Proyecto curricular presentado y aprobado por el equipo de supervisión pedagógica.",
            obs_pastoral="Plan pastoral en revisión por la diócesis de La Plata."
        ),
        AuditoriaIncorporacion(
            nombre="Col. Ntra. Sra. de Luján", congregacion="Hijas de la Cruz", localidad="La Plata", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo2",
            estado="PENDIENTE", estado_pedagogica="PENDIENTE", estado_pastoral="PENDIENTE", estado_economica="PENDIENTE", estado_legal="PENDIENTE"
        ),
        AuditoriaIncorporacion(
            nombre="Col. María Luján Sierra", congregacion="Hijas de la Cruz", localidad="Moreno", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo3",
            estado="EN_PROCESO", estado_pedagogica="COMPLETADO", estado_pastoral="COMPLETADO", estado_economica="OBSERVADO", estado_legal="EN_PROCESO",
            obs_pedagogica="Buen diseño curricular.",
            obs_pastoral="Proyecto pastoral integrado.",
            obs_economica="Se observaron deudas previsionales que deben aclararse antes de continuar.",
            obs_legal="Estatutos legales en revisión."
        ),
        AuditoriaIncorporacion(
            nombre="Col. Ntra. Sra. de Luján", congregacion="Hijas de la Cruz", localidad="Miramar", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo4",
            estado="EN_PROCESO", estado_pedagogica="EN_PROCESO", estado_pastoral="EN_PROCESO", estado_economica="PENDIENTE", estado_legal="PENDIENTE"
        ),
        AuditoriaIncorporacion(
            nombre="Col. Ntra. Sra. de Luján", congregacion="Hijas de la Cruz", localidad="Tres Arroyos", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo5",
            estado="PENDIENTE", estado_pedagogica="PENDIENTE", estado_pastoral="PENDIENTE", estado_economica="PENDIENTE", estado_legal="PENDIENTE"
        ),
        AuditoriaIncorporacion(
            nombre="Hogar San José", congregacion="Hijas de la Cruz", localidad="Tres Arroyos", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo6",
            estado="EN_PROCESO", estado_pedagogica="COMPLETADO", estado_pastoral="COMPLETADO", estado_economica="COMPLETADO", estado_legal="EN_PROCESO",
            obs_pedagogica="Proyecto aprobado.",
            obs_pastoral="Gran arraigo pastoral.",
            obs_economica="Presupuesto equilibrado y balances contables transparentes.",
            obs_legal="Falta constancia de personería jurídica actualizada."
        ),
        AuditoriaIncorporacion(
            nombre="Col. Sagrado Corazón", congregacion="Hijas de la Cruz", localidad="Merlo", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo7",
            estado="EN_PROCESO", estado_pedagogica="COMPLETADO", estado_pastoral="COMPLETADO", estado_economica="PENDIENTE", estado_legal="COMPLETADO"
        ),
        AuditoriaIncorporacion(
            nombre="Col. San José", congregacion="Hijas de la Cruz", localidad="Marcos Paz", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo8",
            estado="PENDIENTE", estado_pedagogica="PENDIENTE", estado_pastoral="PENDIENTE", estado_economica="PENDIENTE", estado_legal="PENDIENTE"
        ),
        AuditoriaIncorporacion(
            nombre="Col. Hnos. Amezola", congregacion="Hijas de la Cruz", localidad="Villa Madero", provincia="Provincia de Buenos Aires",
            drive_folder_url="https://drive.google.com/drive/folders/ejemplo9",
            estado="EN_PROCESO", estado_pedagogica="EN_PROCESO", estado_pastoral="EN_PROCESO", estado_economica="EN_PROCESO", estado_legal="EN_PROCESO"
        )
    ]
    db.add_all(candidatos)

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
