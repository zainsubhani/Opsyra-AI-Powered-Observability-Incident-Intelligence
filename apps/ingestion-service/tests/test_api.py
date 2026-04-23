from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "ingestion-service"


def test_ingest_events() -> None:
    payload = {
        "events": [
            {
                "service_name": "checkout-service",
                "signal_type": "log",
                "severity": "error",
                "message": "database timeout",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "environment": "production",
            }
        ]
    }

    response = client.post("/api/v1/telemetry/events", json=payload)

    assert response.status_code == 202
    body = response.json()
    assert body["accepted_events"] == 1
    assert body["queued_topic"] == "telemetry.raw"
