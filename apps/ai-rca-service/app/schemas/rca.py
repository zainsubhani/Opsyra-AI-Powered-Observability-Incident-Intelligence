from typing import Literal

from pydantic import BaseModel, Field


class RCARequest(BaseModel):
    incident_id: str = Field(..., min_length=3, max_length=50)
    service_name: str = Field(..., min_length=2, max_length=100)
    signal_summary: str = Field(..., min_length=10, max_length=2000)
    suspected_component: str = Field(..., min_length=2, max_length=100)
    severity: Literal["low", "medium", "high", "critical"]

    model_config = {
        "json_schema_extra": {
            "example": {
                "incident_id": "inc_1001",
                "service_name": "payments-service",
                "signal_summary": "Latency and error rates increased immediately after a deploy.",
                "suspected_component": "postgres-primary",
                "severity": "critical",
            }
        }
    }


class RCAResponse(BaseModel):
    incident_id: str
    probable_cause: str
    confidence: float
    remediation_steps: list[str]
    executive_summary: str
