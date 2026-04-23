from datetime import datetime, timezone

from app.schemas.telemetry import IngestionAck, IngestionSummary, TelemetryBatch


def build_ingestion_ack(batch: TelemetryBatch) -> IngestionAck:
    services_seen = sorted({event.service_name for event in batch.events})
    return IngestionAck(
        accepted_events=len(batch.events),
        queued_topic="telemetry.raw",
        received_at=datetime.now(timezone.utc),
        services_seen=services_seen,
    )


def build_ingestion_summary() -> IngestionSummary:
    return IngestionSummary(
        pipeline_status="ready",
        supported_signal_types=["log", "metric", "trace"],
        target_topic="telemetry.raw",
        validation_rules=[
            "service_name is required",
            "signal_type must be log, metric, or trace",
            "batch size must not exceed 500 events",
        ],
    )
