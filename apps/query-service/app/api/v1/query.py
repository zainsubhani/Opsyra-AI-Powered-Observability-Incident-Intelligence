from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.query import IncidentDetailResponse, IncidentListResponse, ServiceOverviewResponse
from app.services.query import get_incident_detail, list_incidents, service_overview
from opsyra_common.database import get_db


router = APIRouter()


@router.get("/incidents", response_model=IncidentListResponse)
def get_incidents(db: Session = Depends(get_db)) -> IncidentListResponse:
    """Return the current incident feed for dashboard and triage workflows."""
    return list_incidents(db)


@router.get("/services/overview", response_model=ServiceOverviewResponse)
def get_service_overview(db: Session = Depends(get_db)) -> ServiceOverviewResponse:
    """Return a compact service health snapshot for the main dashboard."""
    return service_overview(db)


@router.get("/incidents/{incident_id}", response_model=IncidentDetailResponse)
def read_incident_detail(incident_id: str, db: Session = Depends(get_db)) -> IncidentDetailResponse:
    incident = get_incident_detail(db, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found.")
    return incident
