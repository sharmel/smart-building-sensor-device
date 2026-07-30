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


def test_unknown_sensor():
    response = client.get("/sensors/does-not-exist")
    assert response.status_code == 404


def test_invalid_temperature():
    response = client.post(
        "/sensors/readings",
        json={
            "sensor_id": "t1",
            "building_id": "HQ",
            "sensor_type": "temperature",
            "value": 250,
            "timestamp": "2026-07-30T10:00:00Z",
        },
    )
    assert response.status_code == 422


def test_duplicate_timestamp():
    payload = {
        "sensor_id": "t1",
        "building_id": "HQ",
        "sensor_type": "temperature",
        "value": 25,
        "timestamp": "2026-07-30T10:00:00Z",
    }

    client.post("/sensors/readings", json=payload)
    response = client.post("/sensors/readings", json=payload)
    assert response.status_code == 409
