from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.rca import RCARequest, RCAResponse
from app.services.rca import generate_rca
from opsyra_common.auth import require_api_key
from opsyra_common.database import get_db


router = APIRouter()


@router.post("/generate", response_model=RCAResponse, dependencies=[Depends(require_api_key)])
def generate_root_cause_analysis(payload: RCARequest, db: Session = Depends(get_db)) -> RCAResponse:
    """Generate a structured root cause analysis summary for a given incident."""
    return generate_rca(payload, db)
