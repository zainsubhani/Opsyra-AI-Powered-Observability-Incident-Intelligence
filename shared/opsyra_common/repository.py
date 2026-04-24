import json
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from opsyra_common.models import (
    IncidentRecord,
    RcaReportRecord,
    ServiceSnapshotRecord,
    TelemetryEventRecord,
)


def create_telemetry_event(
    db: Session,
    *,
    service_name: str,
    signal_type: str,
    severity: str,
    message: str,
    timestamp: datetime,
    environment: str,
) -> TelemetryEventRecord:
    record = TelemetryEventRecord(
        id=str(uuid4()),
        service_name=service_name,
        signal_type=signal_type,
        severity=severity,
        message=message,
        event_timestamp=timestamp,
        environment=environment,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def mark_telemetry_processed(db: Session, event_id: str) -> None:
    record = db.get(TelemetryEventRecord, event_id)
    if record is None:
        return
    record.processed = True
    record.processed_at = datetime.now(timezone.utc)
    db.add(record)
    db.commit()


def upsert_service_snapshot(
    db: Session,
    *,
    service_name: str,
    health: str,
    open_incidents: int,
    p95_latency_ms: int,
    error_rate_percent: float,
    last_summary: str,
) -> ServiceSnapshotRecord:
    snapshot = db.get(ServiceSnapshotRecord, service_name)
    if snapshot is None:
        snapshot = ServiceSnapshotRecord(service_name=service_name)
    snapshot.health = health
    snapshot.open_incidents = open_incidents
    snapshot.p95_latency_ms = p95_latency_ms
    snapshot.error_rate_percent = error_rate_percent
    snapshot.last_summary = last_summary
    snapshot.updated_at = datetime.now(timezone.utc)
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot


def create_incident(
    db: Session,
    *,
    service_name: str,
    severity: str,
    title: str,
    summary: str,
    source_event_id: str | None,
) -> IncidentRecord:
    incident = IncidentRecord(
        id=str(uuid4()),
        service_name=service_name,
        severity=severity,
        status="open",
        title=title,
        summary=summary,
        source_event_id=source_event_id,
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def list_incidents(db: Session) -> list[IncidentRecord]:
    query = select(IncidentRecord).order_by(desc(IncidentRecord.created_at))
    return list(db.scalars(query))


def list_service_snapshots(db: Session) -> list[ServiceSnapshotRecord]:
    query = select(ServiceSnapshotRecord).order_by(ServiceSnapshotRecord.service_name)
    return list(db.scalars(query))


def get_incident(db: Session, incident_id: str) -> IncidentRecord | None:
    return db.get(IncidentRecord, incident_id)


def save_rca_report(
    db: Session,
    *,
    incident_id: str,
    provider: str,
    model_name: str,
    probable_cause: str,
    executive_summary: str,
    remediation_steps: list[str],
    confidence: float,
) -> RcaReportRecord:
    report = RcaReportRecord(
        id=str(uuid4()),
        incident_id=incident_id,
        provider=provider,
        model_name=model_name,
        probable_cause=probable_cause,
        executive_summary=executive_summary,
        remediation_steps=json.dumps(remediation_steps),
        confidence=confidence,
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def latest_rca_report(db: Session, incident_id: str) -> RcaReportRecord | None:
    query = (
        select(RcaReportRecord)
        .where(RcaReportRecord.incident_id == incident_id)
        .order_by(desc(RcaReportRecord.created_at))
    )
    return db.scalars(query).first()
