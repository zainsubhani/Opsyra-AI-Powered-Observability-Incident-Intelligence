from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.processing import PipelineStatus, ProcessingRequest, ProcessingResult
from app.services.processing import analyze_event, get_pipeline_status
from opsyra_common.database import get_db


router = APIRouter()


@router.post("/analyze", response_model=ProcessingResult)
def analyze_processing_request(
    payload: ProcessingRequest, db: Session = Depends(get_db)
) -> ProcessingResult:
    """Analyze a metric against a baseline and estimate anomaly severity."""
    return analyze_event(payload, db)


@router.get("/status", response_model=PipelineStatus)
def read_pipeline_status() -> PipelineStatus:
    """Return a lightweight snapshot of the processing pipeline state."""
    return get_pipeline_status()
