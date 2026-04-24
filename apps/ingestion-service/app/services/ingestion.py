from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.schemas.telemetry import IngestionAck, IngestionSummary, TelemetryBatch
from opsyra_common.config import get_shared_settings
from opsyra_common.queue import publish_event
from opsyra_common.repository import create_telemetry_event


def build_ingestion_ack(batch: TelemetryBatch, db: Session) -> IngestionAck:
    settings = get_shared_settings()
    services_seen = sorted({event.service_name for event in batch.events})
    published = False
    for event in batch.events:
        record = create_telemetry_event(
            db,
            service_name=event.service_name,
            signal_type=event.signal_type,
            severity=event.severity,
            message=event.message,
            timestamp=event.timestamp,
            environment=event.environment,
        )
        published = (
            publish_event(
                settings.telemetry_stream_name,
                {
                    "event_id": record.id,
                    "service_name": record.service_name,
                    "signal_type": record.signal_type,
                    "severity": record.severity,
                    "message": record.message,
                    "environment": record.environment,
                    "event_timestamp": record.event_timestamp.isoformat(),
                },
            )
            or published
        )
    return IngestionAck(
        accepted_events=len(batch.events),
        queued_topic=settings.telemetry_stream_name,
        queue_status="published" if published else "stored",
        received_at=datetime.now(timezone.utc),
        services_seen=services_seen,
    )


def build_ingestion_summary() -> IngestionSummary:
    settings = get_shared_settings()
    return IngestionSummary(
        pipeline_status="ready",
        supported_signal_types=["log", "metric", "trace"],
        target_topic=settings.telemetry_stream_name,
        validation_rules=[
            "service_name is required",
            "signal_type must be log, metric, or trace",
            "batch size must not exceed 500 events",
        ],
    )
