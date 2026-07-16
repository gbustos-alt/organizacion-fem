# Estándares de Desarrollo y Escalabilidad de Base de Datos
## Ecosistema Digital - Fundación FEM

Este documento establece las pautas de arquitectura, diseño de base de datos y estándares de programación para los desarrolladores de la Fundación FEM. El objetivo es garantizar que la plataforma crezca de manera sostenible, segura y eficiente ante la incorporación de nuevos colegios, directivos, docentes, alumnos y familias.

---

## 1. Arquitectura y Escalabilidad de la Base de Datos

Actualmente la plataforma utiliza **SQLite** en desarrollo, pero la arquitectura de datos está diseñada para migrar directamente a un motor relacional empresarial como **PostgreSQL** en entornos de pre-producción y producción.

### 1.1 Modelo Jerárquico Multitenant (Isolación por Colegio)
Para manejar múltiples colegios de forma simultánea, el ecosistema utiliza un esquema relacional con ámbito delimitado por el ID del colegio.

```
+------------+        +-----------------+        +------------------+
|  Colegios  | <----- |  UsuariosRoles  | -----> |      Roles       |
+------------+        +-----------------+        +------------------+
      |                       |                            |
      |                       v                            v
      |               +-----------------+        +------------------+
      |               |    Usuarios     |        |  RolesPermisos   |
      |               +-----------------+        +------------------+
      |                       |                            |
      v                       v                            v
+------------+        +-----------------+        +------------------+
| Matriculas | <----- |  SesionesActiv  |        |     Permisos     |
+------------+        +-----------------+        +------------------+
```

* **El Colegio como Eje Central:** La tabla `colegios` es la raíz de los datos transaccionales. Todas las entidades que pertenezcan a un colegio específico (Alumnos, Matrículas, Aulas, Calificaciones, etc.) **deben** incluir una clave foránea `colegio_id`.
* **Claves de Indexación Críticas (Foreign Keys & Indexes):**
  Para evitar la degradación de rendimiento en consultas con millones de registros, se deben crear índices explícitos (`index=True`) en:
  - `colegio_id` en todas las tablas secundarias (Alumnos, Matrículas, Auditorías).
  - `usuario_id` en tablas de asignación de roles y sesiones activas.
  - `email` y `username` en la tabla de usuarios (para login ultra rápido).

### 1.2 Transición SQLite a PostgreSQL
En producción, el motor de base de datos se configurará mediante variables de entorno en FastAPI (`DATABASE_URL`).
* **Regla de Código:** Está estrictamente prohibido escribir consultas de SQL plano en formato texto que dependan de dialectos específicos. Utilice siempre el constructor de consultas de **SQLAlchemy ORM** para garantizar la compatibilidad entre motores.
* **Pool de Conexiones:** En producción con PostgreSQL, la configuración debe utilizar un Pool de conexiones adecuado (usando `QueuePool`) con parámetros de timeout y reconexión automática en caso de microcortes de red.

---

## 2. Control de Acceso (RBAC) y Seguridad de Datos

La intranet de la Fundación FEM aloja información sensible (datos personales de menores, balances económicos de colegios, actas de pastoral). El sistema implementa un control de acceso basado en roles con ámbito geográfico/institucional (Scope).

### 2.1 Los Tres Ámbitos de Scope
* **Scope Global (Fundación):** `colegio_id` es `NULL` en la tabla `usuarios_roles`. Permite visualizar y editar la información de toda la red de colegios (reservado para Directivos de la Fundación y Auditores Generales).
* **Scope Escolar Local (Colegio):** `colegio_id` apunta al ID de un colegio específico. El usuario solo puede interactuar con registros asociados a su colegio (Directores Escolares, Secretarios, Auditores Locales).
* **Scope de Aula/Perfil (Docentes/Padres):** Para el crecimiento futuro, los docentes estarán limitados a las asignaturas/grados que dictan, y los padres a las matrículas vinculadas con sus hijos.

### 2.2 Validación en Código (Dependencia FastAPI)
Para proteger un endpoint, inyecte la clase `RequerirPermiso` de `backend.services.rbac_service`:

```python
@router.get("/alumnos", response_class=HTMLResponse)
async def listar_alumnos(
    request: Request,
    db: Session = Depends(get_db),
    user = Depends(RequerirPermiso("alumno", "leer"))
):
    # La dependencia inyecta los colegios a los que el usuario tiene acceso
    scopes = request.state.colegios_permitidos
    
    query = db.query(Alumno)
    if None not in scopes:  # Si no es global, limitar al colegio del scope
        query = query.filter(Alumno.colegio_id.in_(scopes))
        
    alumnos = query.all()
    return templates.TemplateResponse(...)
```

---

## 3. Estándares de Programación para Desarrolladores

### 3.1 Evitar el Problema de Consultas N+1 (joinedload)
Al recuperar listas de registros que poseen relaciones, SQLAlchemy puede ejecutar consultas independientes para recuperar cada relación, colapsando el servidor de base de datos.
* **Estándar:** Utilice `joinedload` (para relaciones 1-a-1) o `subqueryload` (para relaciones 1-a-muchos) si va a mostrar campos de tablas relacionadas en un listado.

```python
# MALA PRÁCTICA (Genera múltiples consultas SELECT en bucle)
usuarios = db.query(Usuario).all()

# BUENA PRÁCTICA (Trae los roles del usuario en una sola consulta JOIN)
from sqlalchemy.orm import joinedload
usuarios = db.query(Usuario).options(joinedload(Usuario.roles_asignados)).all()
```

### 3.2 Manejo de Transacciones Seguro
Las escrituras en base de datos deben realizarse de manera atómica. Ante cualquier fallo del servidor durante una operación de múltiples pasos, se debe garantizar la integridad de los datos.
* **Estándar:** Toda escritura/actualización debe encapsularse en bloques transaccionales y registrarse en la auditoría general de seguridad.

```python
try:
    nuevo_colegio = Colegio(nombre="Nuevo Colegio")
    db.add(nuevo_colegio)
    db.flush() # Genera el ID en la DB sin hacer el commit final
    
    # Registrar auditoría obligatoria
    registrar_accion(
        db=db,
        usuario_id=user.id,
        accion="CREAR",
        recurso="colegio",
        recurso_id=nuevo_colegio.id,
        colegio_id=nuevo_colegio.id,
        valores_nuevos={"nombre": nuevo_colegio.nombre}
    )
    
    db.commit() # Confirmación atómica de ambas operaciones
except Exception as e:
    db.rollback() # Revierte todo en caso de error
    raise HTTPException(status_code=500, detail="Error en la base de datos")
```

### 3.3 Modularidad y Estilo CSS en Frontend
Para mantener un frontend escalable, rápido y con estética premium:
1. **Zero Estilos Inline:** No escriba estilos en línea (`style="..."`) salvo para variables dinámicas de layouts. Utilice clases y tokens definidos en el archivo SCSS.
2. **Uso de Tokens Centralizados:** Toda propiedad visual (colores de fondo, bordes, tipografías) debe usar las variables globales declaradas en `frontend/scss/_tokens.scss`.
   - **Incorrecto:** `background-color: #0c1e36;`
   - **Correcto:** `background-color: var(--color-primary);`
3. **Responsive por Defecto:** Utilice Flexbox o CSS Grid estructurado para layouts. Asegure que los filtros e imágenes utilicen scroll horizontal o layouts en columna mediante `@media` querys para smartphones.
4. **Reusabilidad con Macros:** Si un bloque HTML se repite más de dos veces (ej: botones, headers de páginas, cartas de recursos), defina una Macro en `frontend/templates/components/macros.html` y llámela.

---

## 4. Registro de Auditoría de Transacciones

Cada vez que ocurra un evento de escritura (`CREAR`, `MODIFICAR`, `ELIMINAR`, `APROBAR`), es obligatorio invocar el servicio de auditoría. La tabla `registros_auditoria` guardará:
* Timestamp en UTC.
* ID del usuario y colegio afectado.
* Valores anteriores y nuevos en formato JSON String.
* Dirección IP del cliente para análisis de ciberseguridad.

Este registro es fundamental para garantizar el cumplimiento de normativas de auditoría interna ante el Director Ejecutivo de la FEM y los auditores externos.
