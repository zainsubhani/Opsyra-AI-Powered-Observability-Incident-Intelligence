from app.schemas.processing import PipelineStatus, ProcessingRequest, ProcessingResult
from opsyra_common.config import get_shared_settings
from opsyra_common.repository import create_incident, upsert_service_snapshot
from sqlalchemy.orm import Session


def analyze_event(payload: ProcessingRequest, db: Session) -> ProcessingResult:
    if payload.baseline_value == 0:
        delta_ratio = 1.0
    else:
        delta_ratio = abs(payload.current_value - payload.baseline_value) / abs(payload.baseline_value)

    score = round(min(delta_ratio, 1.0), 2)
    if score >= 0.8:
        severity = "critical"
    elif score >= 0.5:
        severity = "high"
    elif score >= 0.25:
        severity = "medium"
    else:
        severity = "low"

    detected = score >= 0.25
    summary = (
        f"{payload.metric_name} for {payload.service_name} deviated "
        f"from baseline by {round(delta_ratio * 100, 1)}% over the last "
        f"{payload.sample_window_minutes} minutes."
    )

    result = ProcessingResult(
        service_name=payload.service_name,
        metric_name=payload.metric_name,
        anomaly_score=score,
        anomaly_detected=detected,
        severity=severity,
        summary=summary,
    )
    if detected:
        create_incident(
            db,
            service_name=payload.service_name,
            severity=severity,
            title=f"{payload.service_name} anomaly detected",
            summary=summary,
            source_event_id=None,
        )
        upsert_service_snapshot(
            db,
            service_name=payload.service_name,
            health="down" if severity == "critical" else "degraded",
            open_incidents=1,
            p95_latency_ms=int(payload.current_value),
            error_rate_percent=round(score * 10, 2),
            last_summary=summary,
        )
    return result


def get_pipeline_status() -> PipelineStatus:
    settings = get_shared_settings()
    return PipelineStatus(
        pipeline_state="running",
        active_detectors=["latency_spike", "error_rate_jump", "throughput_drop"],
        output_topics=[settings.telemetry_stream_name, "incidents.open"],
        consumer_enabled=settings.processing_enable_consumer,
    )
