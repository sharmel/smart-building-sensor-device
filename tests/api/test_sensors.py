from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200


def test_sensor_not_found():
    response = client.get("/sensors/unknown")

    assert response.status_code == 404


def test_post_sensor():
    response = client.post(
        "/sensors/readings",
        json={
            "sensor_id": "temp-1",
            "building_id": "HQ",
            "sensor_type": "temperature",
            "value": 20,
            "timestamp": "2026-07-30T10:00:00Z",
        },
    )

    assert response.status_code == 202
