from fastapi import APIRouter

from app.schemas.processing import PipelineStatus, ProcessingRequest, ProcessingResult
from app.services.processing import analyze_event, get_pipeline_status


router = APIRouter()


@router.post("/analyze", response_model=ProcessingResult)
def analyze_processing_request(payload: ProcessingRequest) -> ProcessingResult:
    """Analyze a metric against a baseline and estimate anomaly severity."""
    return analyze_event(payload)


@router.get("/status", response_model=PipelineStatus)
def read_pipeline_status() -> PipelineStatus:
    """Return a lightweight snapshot of the processing pipeline state."""
    return get_pipeline_status()
