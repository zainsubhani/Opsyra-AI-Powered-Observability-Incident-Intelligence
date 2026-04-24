from fastapi.testclient import TestClient

from app.main import app
from opsyra_common.database import SessionLocal, init_database
from opsyra_common.models import IncidentRecord, ServiceSnapshotRecord
from opsyra_common.repository import create_incident, upsert_service_snapshot


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json()["service"] == "query-service"


def test_get_incidents() -> None:
    init_database()
    db = SessionLocal()
    try:
        db.query(IncidentRecord).delete()
        db.query(ServiceSnapshotRecord).delete()
        db.commit()
        create_incident(
            db,
            service_name="payments-service",
            severity="critical",
            title="Payment API latency spike",
            summary="Latency crossed 600ms for the payments service.",
            source_event_id=None,
        )
        upsert_service_snapshot(
            db,
            service_name="payments-service",
            health="degraded",
            open_incidents=1,
            p95_latency_ms=620,
            error_rate_percent=4.1,
            last_summary="Latency crossed 600ms for the payments service.",
        )
    finally:
        db.close()

    response = client.get("/api/v1/query/incidents")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] >= 1
    assert len(body["incidents"][0]["incident_id"]) > 10
