from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_analyze_endpoint():
    response = client.post("/api/v1/analyze", json={"filename": "acctrec.pli", "content": "ACCTREC: PROC;\nIF AMOUNT > 0 THEN\nTAX = AMOUNT * RATE;"})
    assert response.status_code == 200
    assert response.json()["language"] == "pli"
