import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "أدوات" in response.text

def test_process_tashkeel():
    response = client.post(
        "/api/v1/process",
        json={"text": "الشمس", "action": "tashkeel"}
    )
    assert response.status_code == 200
    assert "result" in response.json()
    assert "الشَّمْس" in response.json()["result"]

def test_process_invalid_action():
    response = client.post(
        "/api/v1/process",
        json={"text": "test", "action": "invalid_action"}
    )
    assert response.status_code == 400
