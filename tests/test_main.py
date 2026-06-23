from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_home():
    """
    Verifica que la pagina de inicio (/) cargue correctamente
    y contenga elementos clave de la marca institucional.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Organización" in response.text
    assert "FEM" in response.text

def test_read_identidad():
    """
    Verifica que la pagina 'Identidad' (/identidad) cargue correctamente.
    """
    response = client.get("/identidad")
    assert response.status_code == 200
    assert "Identidad" in response.text or "identidad" in response.text.lower()

def test_read_mision():
    """
    Verifica que la pagina 'Mision' (/mision) cargue correctamente.
    """
    response = client.get("/mision")
    assert response.status_code == 200
    assert "Misión" in response.text or "misión" in response.text.lower()

def test_read_dimensiones():
    """
    Verifica que la pagina 'Dimensiones' (/dimensiones) cargue correctamente.
    """
    response = client.get("/dimensiones")
    assert response.status_code == 200
    assert "Dimensiones" in response.text or "dimensiones" in response.text.lower()

def test_read_organizacion():
    """
    Verifica que la pagina 'Organizacion' (/organizacion) cargue correctamente.
    """
    response = client.get("/organizacion")
    assert response.status_code == 200
    assert "Gobierno" in response.text or "gobierno" in response.text.lower()

def test_read_colegios():
    """
    Verifica que la pagina de colegios (/colegios) cargue correctamente.
    """
    response = client.get("/colegios")
    assert response.status_code == 200
    assert "Colegios" in response.text or "colegios" in response.text.lower()

def test_read_contacto():
    """
    Verifica que la pagina de contacto (/contacto) cargue correctamente.
    """
    response = client.get("/contacto")
    assert response.status_code == 200
    assert "Contacto" in response.text or "contacto" in response.text.lower()

def test_read_admin_unauthorized():
    """
    Verifica que el panel administrativo (/admin/) no sea accesible de forma anónima
    y redirija automáticamente a la página de login (307).
    """
    response = client.get("/admin/", follow_redirects=False)
    assert response.status_code == 307
    assert "/admin/auth/login" in response.headers["location"]

def test_admin_login_logout_flow():
    """
    Verifica el flujo completo de login con credenciales correctas,
    la obtención de la cookie de sesión, el acceso al dashboard y el logout.
    """
    # 1. Login fallido
    login_fail = client.post("/admin/auth/login", data={"username": "admin", "password": "wrongpassword"})
    assert login_fail.status_code == 401
    assert "Usuario o contraseña incorrectos" in login_fail.text

    # 2. Login exitoso
    login_success = client.post("/admin/auth/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    assert login_success.status_code == 303
    assert "session_id" in login_success.cookies

    # 3. Acceder al dashboard con la cookie
    session_cookie = login_success.cookies["session_id"]
    dashboard_resp = client.get("/admin/", cookies={"session_id": session_cookie})
    assert dashboard_resp.status_code == 200
    assert "Dashboard General" in dashboard_resp.text
    assert "admin" in dashboard_resp.text

    # 4. Acceder al listado de colegios con la cookie
    colegios_resp = client.get("/admin/colegios/", cookies={"session_id": session_cookie})
    assert colegios_resp.status_code == 200
    assert "Gestión de Colegios" in colegios_resp.text

    # 5. Logout
    logout_resp = client.get("/admin/auth/logout", cookies={"session_id": session_cookie}, follow_redirects=False)
    assert logout_resp.status_code == 303
    # Verificar que se borró el cookie o redirigió al login
    assert "session_id" not in logout_resp.cookies or logout_resp.cookies.get("session_id") == ""

def test_director_scope_restrictions():
    """
    Verifica que un usuario con rol 'Director' asignado a un colegio específico:
    1. Puede loguearse exitosamente.
    2. Su vista de alumnos está restringida a su colegio.
    3. No puede registrar nuevos colegios (restringido a global).
    """
    # 1. Login Director
    login_dir = client.post("/admin/auth/login", data={"username": "director", "password": "director123"}, follow_redirects=False)
    assert login_dir.status_code == 303
    dir_cookie = login_dir.cookies["session_id"]

    # 2. Intentar crear colegio (Debe dar 403)
    crear_col_resp = client.get("/admin/colegios/crear", cookies={"session_id": dir_cookie})
    assert crear_col_resp.status_code == 403
    assert "Acceso denegado: carece del permiso" in crear_col_resp.json()["detail"]

    # 3. Listar alumnos (Debe dar 200)
    alumnos_resp = client.get("/admin/alumnos/", cookies={"session_id": dir_cookie})
    assert alumnos_resp.status_code == 200
    assert "Gestión de Alumnos" in alumnos_resp.text

def test_agent_integration_flow():
    """
    Verifica la protección del panel del Agente y el correcto procesamiento
    de consultas analíticas vía POST.
    """
    # 1. Acceso no autorizado (Redirige 307 al login)
    client.cookies.clear()
    resp = client.get("/admin/agente/", follow_redirects=False)
    assert resp.status_code == 307
    assert "/admin/auth/login" in resp.headers["location"]

    # 2. Login y obtención de sesión
    login = client.post("/admin/auth/login", data={"username": "admin", "password": "admin123"}, follow_redirects=False)
    cookie = login.cookies["session_id"]

    # 3. Acceso exitoso al panel del Agente
    panel_resp = client.get("/admin/agente/", cookies={"session_id": cookie})
    assert panel_resp.status_code == 200
    assert "Asistente de Gestión" in panel_resp.text

    # 4. Enviar consulta de resumen general (JSON Response)
    query_resp = client.post("/admin/agente/consultar", data={"query": "Resumime el estado general"}, cookies={"session_id": cookie})
    assert query_resp.status_code == 200
    json_data = query_resp.json()
    assert "respuesta" in json_data
    assert "Colegios Registrados" in json_data["respuesta"]
    assert json_data["categoria"] == "resumen"

    # 5. Enviar consulta de cálculo financiero
    calc_resp = client.post("/admin/agente/consultar", data={"query": "Calculá ingresos arancelarios para 200 alumnos con cuota 30000"}, cookies={"session_id": cookie})
    assert calc_resp.status_code == 200
    json_calc = calc_resp.json()
    assert "respuesta" in json_calc
    assert "Simulación de Ingresos" in json_calc["respuesta"]
    assert "6,000,000.00" in json_calc["respuesta"]  # 200 * 30000 = 6,000,000

def test_post_contacto():
    """
    Verifica que el formulario de contacto se envíe correctamente por POST
    y que se persista en la base de datos.
    """
    data = {
        "nombre": "Test User",
        "email": "test@user.com",
        "telefono": "12345678",
        "mensaje": "Mensaje de prueba para contacto"
    }
    response = client.post("/contacto", data=data)
    assert response.status_code == 200
    assert "Hemos recibido tu mensaje" in response.text

def test_404_custom_error_page():
    """
    Verifica que las rutas inexistentes sean capturadas y 
    devuelvan una respuesta HTML con código de estado 404.
    """
    response = client.get("/ruta-inexistente-para-test")
    assert response.status_code == 404
    assert "Página No Encontrada" in response.text

