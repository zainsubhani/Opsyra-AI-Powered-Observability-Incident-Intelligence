from fastapi.testclient import TestClient

from app.main import app
from opsyra_common.database import init_database


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "processing-service"


def test_analyze_processing_request() -> None:
    init_database()
    payload = {
        "service_name": "payments-service",
        "metric_name": "p95_latency_ms",
        "current_value": 480,
        "baseline_value": 200,
        "sample_window_minutes": 15,
    }

    response = client.post("/api/v1/processing/analyze", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["anomaly_detected"] is True
    assert body["severity"] in {"high", "critical"}
