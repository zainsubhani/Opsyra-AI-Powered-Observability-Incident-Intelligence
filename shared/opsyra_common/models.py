from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text

from opsyra_common.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class TelemetryEventRecord(Base):
    __tablename__ = "telemetry_events"

    id = Column(String(36), primary_key=True)
    service_name = Column(String(100), index=True, nullable=False)
    signal_type = Column(String(20), index=True, nullable=False)
    severity = Column(String(20), index=True, nullable=False)
    message = Column(Text(), nullable=False)
    event_timestamp = Column(DateTime(timezone=True), index=True, nullable=False)
    environment = Column(String(50), default="production", nullable=False)
    processed = Column(Boolean(), default=False, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    processed_at = Column(DateTime(timezone=True), nullable=True)


class IncidentRecord(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True)
    service_name = Column(String(100), index=True, nullable=False)
    severity = Column(String(20), index=True, nullable=False)
    status = Column(String(20), default="open", index=True, nullable=False)
    title = Column(String(255), nullable=False)
    summary = Column(Text(), nullable=False)
    probable_cause = Column(Text(), nullable=True)
    source_event_id = Column(String(36), ForeignKey("telemetry_events.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class ServiceSnapshotRecord(Base):
    __tablename__ = "service_snapshots"

    service_name = Column(String(100), primary_key=True)
    health = Column(String(20), default="healthy", nullable=False)
    open_incidents = Column(Integer(), default=0, nullable=False)
    p95_latency_ms = Column(Integer(), default=0, nullable=False)
    error_rate_percent = Column(Float(), default=0.0, nullable=False)
    last_summary = Column(Text(), nullable=True)
    updated_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)


class RcaReportRecord(Base):
    __tablename__ = "rca_reports"

    id = Column(String(36), primary_key=True)
    incident_id = Column(String(36), ForeignKey("incidents.id"), index=True, nullable=False)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(100), nullable=False)
    probable_cause = Column(Text(), nullable=False)
    executive_summary = Column(Text(), nullable=False)
    remediation_steps = Column(Text(), nullable=False)
    confidence = Column(Float(), default=0.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
