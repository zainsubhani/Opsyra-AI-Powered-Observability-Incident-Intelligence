from fastapi import APIRouter

from app.schemas.rca import RCARequest, RCAResponse
from app.services.rca import generate_rca


router = APIRouter()


@router.post("/generate", response_model=RCAResponse)
def generate_root_cause_analysis(payload: RCARequest) -> RCAResponse:
    """Generate a structured root cause analysis summary for a given incident."""
    return generate_rca(payload)
