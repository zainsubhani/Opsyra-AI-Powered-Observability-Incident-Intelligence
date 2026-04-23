from app.schemas.processing import PipelineStatus, ProcessingRequest, ProcessingResult


def analyze_event(payload: ProcessingRequest) -> ProcessingResult:
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

    return ProcessingResult(
        service_name=payload.service_name,
        metric_name=payload.metric_name,
        anomaly_score=score,
        anomaly_detected=detected,
        severity=severity,
        summary=summary,
    )


def get_pipeline_status() -> PipelineStatus:
    return PipelineStatus(
        pipeline_state="running",
        active_detectors=["latency_spike", "error_rate_jump", "throughput_drop"],
        output_topics=["telemetry.enriched", "incidents.candidates"],
    )
