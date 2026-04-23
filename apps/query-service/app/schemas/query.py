from typing import Literal

from pydantic import BaseModel


class IncidentItem(BaseModel):
    incident_id: str
    service_name: str
    severity: Literal["low", "medium", "high", "critical"]
    status: Literal["open", "investigating", "resolved"]
    title: str


class IncidentListResponse(BaseModel):
    incidents: list[IncidentItem]
    total: int


class ServiceOverviewItem(BaseModel):
    service_name: str
    health: Literal["healthy", "degraded", "down"]
    open_incidents: int
    p95_latency_ms: int
    error_rate_percent: float


class ServiceOverviewResponse(BaseModel):
    services: list[ServiceOverviewItem]
    generated_from: str
