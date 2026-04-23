from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "ai-rca-service"


def test_generate_root_cause_analysis() -> None:
    payload = {
        "incident_id": "inc_1001",
        "service_name": "payments-service",
        "signal_summary": "Latency and error rates increased immediately after a deploy.",
        "suspected_component": "postgres-primary",
        "severity": "critical",
    }

    response = client.post("/api/v1/rca/generate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["incident_id"] == "inc_1001"
    assert len(body["remediation_steps"]) == 3
