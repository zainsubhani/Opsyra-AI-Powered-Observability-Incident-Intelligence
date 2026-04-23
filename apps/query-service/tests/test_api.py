from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "query-service"


def test_get_incidents() -> None:
    response = client.get("/api/v1/query/incidents")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert body["incidents"][0]["incident_id"].startswith("inc_")
