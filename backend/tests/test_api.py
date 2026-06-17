from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

SCHEMA = {"ingreso_familiar": "numero", "promedio": "numero",
          "integrantes_familia": "numero", "distancia_km": "numero"}


def test_flujo_completo():
    r = client.post("/reglas", json={
        "texto": "SI ingreso_familiar < 300000 Y promedio >= 7 ENTONCES elegible",
        "schema_vars": SCHEMA,
    })
    assert r.status_code == 200

    r = client.post("/postulantes", json={"postulantes": [
        {"id": 1, "ingreso_familiar": 100000, "promedio": 9, "integrantes_familia": 5, "distancia_km": 80},
        {"id": 2, "ingreso_familiar": 500000, "promedio": 9, "integrantes_familia": 1, "distancia_km": 2},
        {"id": 3, "ingreso_familiar": 250000, "promedio": 8, "integrantes_familia": 2, "distancia_km": 10},
    ]})
    assert r.status_code == 200

    r = client.post("/evaluar", json={})
    assert r.status_code == 200
    data = r.json()
    ids_ranking = [p["id"] for p in data["ranking"]]
    assert ids_ranking == [1, 3]
    assert data["ranking"][0]["score"] >= data["ranking"][1]["score"]
    assert "certificado" in data["ranking"][0]


def test_regla_invalida_da_400():
    r = client.post("/reglas", json={
        "texto": "SI inexistente < 5 ENTONCES elegible",
        "schema_vars": SCHEMA,
    })
    assert r.status_code == 400
