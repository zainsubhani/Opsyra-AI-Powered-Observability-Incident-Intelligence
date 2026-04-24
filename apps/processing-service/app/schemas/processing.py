from typing import Literal

from pydantic import BaseModel, Field


class ProcessingRequest(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=100)
    metric_name: str = Field(..., min_length=2, max_length=100)
    current_value: float
    baseline_value: float
    sample_window_minutes: int = Field(default=15, ge=1, le=1440)

    model_config = {
        "json_schema_extra": {
            "example": {
                "service_name": "payments-service",
                "metric_name": "p95_latency_ms",
                "current_value": 480,
                "baseline_value": 200,
                "sample_window_minutes": 15,
            }
        }
    }


class ProcessingResult(BaseModel):
    service_name: str
    metric_name: str
    anomaly_score: float
    anomaly_detected: bool
    severity: Literal["low", "medium", "high", "critical"]
    summary: str


class PipelineStatus(BaseModel):
    pipeline_state: str
    active_detectors: list[str]
    output_topics: list[str]
    consumer_enabled: bool
