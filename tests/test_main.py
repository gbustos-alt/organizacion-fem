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
