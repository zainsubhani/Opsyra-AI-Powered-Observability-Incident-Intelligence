from app.schemas.query import (
    IncidentDetailResponse,
    IncidentItem,
    IncidentListResponse,
    ServiceOverviewItem,
    ServiceOverviewResponse,
)
from opsyra_common.repository import get_incident, list_incidents as repo_list_incidents
from opsyra_common.repository import list_service_snapshots
from sqlalchemy.orm import Session


def list_incidents(db: Session) -> IncidentListResponse:
    incidents = [
        IncidentItem(
            incident_id=incident.id,
            service_name=incident.service_name,
            severity=incident.severity,
            status=incident.status,
            title=incident.title,
        )
        for incident in repo_list_incidents(db)
    ]
    return IncidentListResponse(incidents=incidents, total=len(incidents))


def service_overview(db: Session) -> ServiceOverviewResponse:
    services = [
        ServiceOverviewItem(
            service_name=item.service_name,
            health=item.health,
            open_incidents=item.open_incidents,
            p95_latency_ms=item.p95_latency_ms,
            error_rate_percent=item.error_rate_percent,
        )
        for item in list_service_snapshots(db)
    ]
    return ServiceOverviewResponse(services=services, generated_from="postgresql")


def get_incident_detail(db: Session, incident_id: str) -> IncidentDetailResponse | None:
    incident = get_incident(db, incident_id)
    if incident is None:
        return None
    return IncidentDetailResponse(
        incident_id=incident.id,
        service_name=incident.service_name,
        severity=incident.severity,
        status=incident.status,
        title=incident.title,
        summary=incident.summary,
        probable_cause=incident.probable_cause,
    )
