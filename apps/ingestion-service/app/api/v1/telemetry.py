from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.telemetry import IngestionAck, IngestionSummary, TelemetryEvent, TelemetryBatch
from app.services.ingestion import build_ingestion_ack, build_ingestion_summary
from opsyra_common.auth import require_api_key
from opsyra_common.database import get_db


router = APIRouter()


@router.post(
    "/events",
    response_model=IngestionAck,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_api_key)],
)
def ingest_events(batch: TelemetryBatch, db: Session = Depends(get_db)) -> IngestionAck:
    """Accept a batch of telemetry events and acknowledge queuing details."""
    return build_ingestion_ack(batch, db)


@router.get("/summary", response_model=IngestionSummary)
def get_ingestion_summary() -> IngestionSummary:
    """Return the current ingestion contract and pipeline expectations."""
    return build_ingestion_summary()


@router.post(
    "/event",
    response_model=IngestionAck,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_api_key)],
)
def ingest_single_event(event: TelemetryEvent, db: Session = Depends(get_db)) -> IngestionAck:
    """Submit a single telemetry event for quick live testing in Swagger UI."""
    return build_ingestion_ack(TelemetryBatch(events=[event]), db)
