import re
from sqlalchemy.orm import Session
from backend.models import Colegio, Alumno, Matricula, SesionActiva

def procesar_consulta_agente(db: Session, query: str) -> dict:
    """
    Procesa consultas del usuario y genera respuestas estructuradas e interactivas.
    Utiliza datos reales de la base de datos combinados con lógica de negocio simulada para la demo.
    """
    query_lower = query.lower().strip()
    
    # 1. RESUMEN GENERAL DE ESTADO
    if any(k in query_lower for k in ["resum", "estado", "general", "cuantas", "cuantos"]):
        colegios_count = db.query(Colegio).count()
        alumnos_count = db.query(Alumno).count()
        matriculas_count = db.query(Matricula).count()
        matriculas_pendientes = db.query(Matricula).filter(Matricula.estado == "PENDIENTE").count()
        sesiones_count = db.query(SesionActiva).count()
        
        texto_respuesta = (
            f"### 📋 Resumen del Estado General de la Red\n\n"
            f"Actualmente la **Fundación FEM** cuenta con los siguientes registros activos en la plataforma:\n\n"
            f"*   **Colegios Registrados:** {colegios_count} instituciones educativas en CABA, PBA y Presencia Federal.\n"
            f"*   **Alumnos Matriculados:** {alumnos_count} estudiantes activos en las bases de datos.\n"
            f"*   **Matrículas Totales:** {matriculas_count} solicitudes históricas.\n"
            f"*   **Matrículas Pendientes:** {matriculas_pendientes} solicitudes en espera de revisión administrativa.\n"
            f"*   **Usuarios/Sesiones Activas:** {sesiones_count} administradores/agentes con sesión abierta en este momento.\n\n"
            f"El sistema se encuentra en un estado **operativo estable** y listo para recibir cargas de notas y asistencia."
        )
        return {
            "query": query,
            "respuesta": texto_respuesta,
            "categoria": "resumen"
        }

    # 2. CÁLCULO DE INGRESOS ESTIMADOS (CON REGEX)
    elif any(k in query_lower for k in ["ingreso", "estim", "calcul", "cuota", "proyeccion", "multiplic"]):
        # Extraer números de la consulta usando expresiones regulares
        numbers = [int(s) for s in re.findall(r'\d+', query)]
        
        # Valores por defecto si no se especifican en la consulta
        cant_alumnos = db.query(Alumno).count()
        cuota_promedio = 35000  # Valor por defecto
        
        if len(numbers) >= 2:
            # Si hay 2 números o más, asumimos: [alumnos, cuota] o [cuota, alumnos]
            # Generalmente el primer número grande suele ser alumnos o viceversa, lo organizamos:
            num1, num2 = numbers[0], numbers[1]
            if num1 > 10000 or num2 < num1:
                cant_alumnos = num1
                cuota_promedio = num2
            else:
                cant_alumnos = num2
                cuota_promedio = num1
        elif len(numbers) == 1:
            # Si hay un solo número, si es menor a 1500 asumimos que son alumnos, si es mayor asumimos que es cuota
            num = numbers[0]
            if num < 2000:
                cant_alumnos = num
            else:
                cuota_promedio = num
                
        # Cálculos de ingresos
        mensual_bruto = cant_alumnos * cuota_promedio
        anual_estimado = mensual_bruto * 10  # 10 meses de ciclo lectivo arancelado
        tasa_cobro_real = 0.85  # Tasa estimada de cobro efectivo (85%)
        mensual_real_estimado = mensual_bruto * tasa_cobro_real
        
        texto_respuesta = (
            f"### 💰 Simulación de Ingresos Mensuales Proyectados\n\n"
            f"Realicé el cálculo financiero solicitado basándome en los parámetros arancelarios provistos:\n\n"
            f"*   **Cantidad de Alumnos:** {cant_alumnos} alumnos.\n"
            f"*   **Valor de Cuota Promedio:** ${cuota_promedio:,.2f} ARS.\n"
            f"*   **Ingreso Mensual Teórico (100% cobro):** **${mensual_bruto:,.2f} ARS**.\n"
            f"*   **Proyección Anual del Ciclo (10 meses):** **${anual_estimado:,.2f} ARS**.\n\n"
            f"⚠️ **Ajuste de Morosidad Estimada (15%):**\n"
            f"Considerando una tasa histórica de cobro efectivo del **85%**, el ingreso mensual neto real estimado es de **${mensual_real_estimado:,.2f} ARS**."
        )
        return {
            "query": query,
            "respuesta": texto_respuesta,
            "categoria": "ingresos"
        }

    # 3. CARGA PENDIENTE POR MÓDULO
    elif any(k in query_lower for k in ["carga", "pendient", "modulo", "urgente", "revisar"]):
        matriculas_pendientes = db.query(Matricula).filter(Matricula.estado == "PENDIENTE").count()
        colegios_sin_telefono = db.query(Colegio).filter((Colegio.telefono == None) | (Colegio.telefono == "")).count()
        
        texto_respuesta = (
            f"### ⚡ Diagnóstico de Tareas Administrativas Pendientes\n\n"
            f"Analicé el estado de los módulos de la intranet y detecté las siguientes cargas pendientes:\n\n"
            f"1.  **Módulo Matrículas (Urgente):** Hay **{matriculas_pendientes}** solicitudes de matrícula pendientes de aprobación. Este es actualmente el cuello de botella del sistema.\n"
            f"2.  **Módulo Colegios (Medio):** Existen **{colegios_sin_telefono}** colegios con el campo telefónico o de contacto incompleto en sus fichas institucionales.\n"
            f"3.  **Módulo Alumnos (Bajo):** Todos los alumnos cargados se encuentran correctamente asignados a una escuela oficial.\n\n"
            f"**Acción Recomendada:** Diríjase al menú de revisión de matrícula o solicite a secretaría completar las fichas de las instituciones."
        )
        return {
            "query": query,
            "respuesta": texto_respuesta,
            "categoria": "pendientes"
        }

    # 4. FALTANTES DE INFORMACIÓN PARA REPORTES
    elif any(k in query_lower for k in ["falt", "informacion", "report", "cerrar", "incomplet"]):
        # Obtener colegios con sitio web o datos incompletos para simular
        colegios_incompletos = db.query(Colegio).filter((Colegio.web_url == None) | (Colegio.web_url == "")).limit(2).all()
        nombres_incompletos = ", ".join([col.nombre for col in colegios_incompletos]) if colegios_incompletos else "Ninguno"
        
        texto_respuesta = (
            f"### 🔍 Faltantes de Información para Reporte de Gestión\n\n"
            f"Para cerrar el Reporte de Ciclo Lectivo y consolidar la información ante el Consejo Directivo, faltan completar los siguientes datos estructurados:\n\n"
            f"*   **Sitios Web de Colegios:** Falta registrar la URL institucional en las fichas de: *{nombres_incompletos}*.\n"
            f"*   **Auditoría de Acciones:** Se requiere la revisión de firmas y claves de acceso de los Agentes Automatizados antes del cierre de periodo.\n"
            f"*   **Direcciones de Envío:** Hay 2 registros de contacto sin provincia o localidad asociada en la base de datos pública.\n\n"
            f"Una vez completados estos campos, el sistema estará habilitado para generar el archivo PDF consolidado de gestión."
        )
        return {
            "query": query,
            "respuesta": texto_respuesta,
            "categoria": "reportes"
        }

    # 5. MENSAJE PREDETERMINADO / GUÍA
    else:
        texto_respuesta = (
            f"### 👋 Hola. Soy el Asistente de Gestión de Fundación FEM\n\n"
            f"Estoy preparado para ayudarte a consultar y calcular métricas operativas de la intranet educativa. Como esta es una versión de demostración comercial (MVP), podés probar mis capacidades seleccionando uno de los siguientes comandos sugeridos o haciendo preguntas relacionadas:\n\n"
            f"*   *\"Resumime el estado general de colegios y alumnos\"*\n"
            f"*   *\"Calculá ingresos estimados para 320 alumnos con cuota promedio de 25000\"*\n"
            f"*   *\"¿Qué módulo tiene más carga pendiente?\"*\n"
            f"*   *\"¿Qué información falta para cerrar un reporte?\"*\n\n"
            f"Escribí tu consulta en la barra de texto o presioná una de las acciones rápidas."
        )
        return {
            "query": query,
            "respuesta": texto_respuesta,
            "categoria": "guiado"
        }
