from fastapi.testclient import TestClient

from app.main import app
from opsyra_common.database import SessionLocal, init_database
from opsyra_common.models import IncidentRecord, RcaReportRecord
from opsyra_common.repository import create_incident


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "ai-rca-service"


def test_generate_root_cause_analysis() -> None:
    init_database()
    db = SessionLocal()
    try:
        db.query(RcaReportRecord).delete()
        db.query(IncidentRecord).delete()
        db.commit()
        incident = create_incident(
            db,
            service_name="payments-service",
            severity="critical",
            title="Payment API latency spike",
            summary="Latency and error rates increased immediately after a deploy.",
            source_event_id=None,
        )
    finally:
        db.close()

    payload = {"incident_id": incident.id}

    response = client.post("/api/v1/rca/generate", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["incident_id"] == incident.id
    assert len(body["remediation_steps"]) == 3
    assert body["provider"] in {"heuristic", "openai"}
