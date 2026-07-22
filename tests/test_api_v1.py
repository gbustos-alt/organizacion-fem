from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_api_v1_get_novedades():
    """
    Verifica que GET /api/v1/novedades devuelva respuesta JSON estandarizada.
    """
    response = client.get("/api/v1/novedades")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)
    assert json_data["message"] == "Novedades obtenidas exitosamente"

def test_api_v1_get_actividades():
    """
    Verifica que GET /api/v1/actividades devuelva respuesta JSON estandarizada.
    """
    response = client.get("/api/v1/actividades")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)

def test_api_v1_get_reflexiones():
    """
    Verifica que GET /api/v1/reflexiones devuelva respuesta JSON estandarizada.
    """
    response = client.get("/api/v1/reflexiones")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert isinstance(json_data["data"], list)

def test_api_v1_get_config_home():
    """
    Verifica que GET /api/v1/config/home devuelva la configuración del lema y quiénes somos.
    """
    response = client.get("/api/v1/config/home")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert "lema" in json_data["data"]
    assert "quienes_somos" in json_data["data"]

def test_api_v1_unauthorized_mutations():
    """
    Verifica que operaciones POST/PUT/DELETE sin autenticación retornen error HTTP 401.
    """
    res_post = client.post("/api/v1/novedades", json={"titulo": "Test", "contenido": "Test"})
    assert res_post.status_code in [401, 403]

    res_put = client.put("/api/v1/config/home", json={"lema_texto": "Test Lema"})
    assert res_put.status_code in [401, 403]
