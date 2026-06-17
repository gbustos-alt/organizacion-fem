from fastapi.testclient import TestClient
from app.main import app

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

def test_read_nosotros():
    """
    Verifica que la pagina 'Nosotros' (/nosotros) cargue correctamente.
    """
    response = client.get("/nosotros")
    assert response.status_code == 200
    assert "Sobre Nosotros" in response.text

def test_read_admin_placeholder():
    """
    Verifica que el panel administrativo (/admin/) cargue correctamente.
    """
    response = client.get("/admin/")
    assert response.status_code == 200
    assert "Panel Administrativo" in response.text

def test_404_custom_error_page():
    """
    Verifica que las rutas inexistentes sean capturadas y 
    devuelvan una respuesta HTML con codigo de estado 404.
    """
    response = client.get("/ruta-inexistente-para-test")
    assert response.status_code == 404
    assert "Página No Encontrada" in response.text
