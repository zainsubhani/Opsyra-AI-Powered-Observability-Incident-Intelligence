from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    service_name: str = Field(..., min_length=2, max_length=100)
    signal_type: Literal["log", "metric", "trace"]
    severity: Literal["debug", "info", "warning", "error", "critical"] = "info"
    message: str = Field(..., min_length=1, max_length=1000)
    timestamp: datetime
    environment: str = Field(default="production", min_length=2, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "service_name": "checkout-service",
                "signal_type": "log",
                "severity": "error",
                "message": "Database timeout while creating order 42.",
                "timestamp": "2026-04-23T12:30:00Z",
                "environment": "production",
            }
        }
    }


class TelemetryBatch(BaseModel):
    events: list[TelemetryEvent] = Field(..., min_length=1, max_length=500)

    model_config = {
        "json_schema_extra": {
            "example": {
                "events": [
                    {
                        "service_name": "checkout-service",
                        "signal_type": "log",
                        "severity": "error",
                        "message": "Database timeout while creating order 42.",
                        "timestamp": "2026-04-23T12:30:00Z",
                        "environment": "production",
                    },
                    {
                        "service_name": "payments-service",
                        "signal_type": "metric",
                        "severity": "warning",
                        "message": "p95 latency crossed 450ms.",
                        "timestamp": "2026-04-23T12:31:00Z",
                        "environment": "production",
                    },
                ]
            }
        }
    }


class IngestionAck(BaseModel):
    accepted_events: int
    queued_topic: str
    queue_status: str
    received_at: datetime
    services_seen: list[str]


class IngestionSummary(BaseModel):
    pipeline_status: str
    supported_signal_types: list[str]
    target_topic: str
    validation_rules: list[str]
