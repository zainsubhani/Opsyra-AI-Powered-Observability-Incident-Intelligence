from fastapi import APIRouter

from app.schemas.query import IncidentListResponse, ServiceOverviewResponse
from app.services.query import list_incidents, service_overview


router = APIRouter()


@router.get("/incidents", response_model=IncidentListResponse)
def get_incidents() -> IncidentListResponse:
    """Return the current incident feed for dashboard and triage workflows."""
    return list_incidents()


@router.get("/services/overview", response_model=ServiceOverviewResponse)
def get_service_overview() -> ServiceOverviewResponse:
    """Return a compact service health snapshot for the main dashboard."""
    return service_overview()
