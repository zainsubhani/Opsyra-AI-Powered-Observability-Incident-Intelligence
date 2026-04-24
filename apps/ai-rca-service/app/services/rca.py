from sqlalchemy.orm import Session

from app.schemas.rca import RCARequest, RCAResponse
from opsyra_common.rca_provider import generate_rca_from_model
from opsyra_common.repository import get_incident, save_rca_report


def generate_rca(payload: RCARequest, db: Session) -> RCAResponse:
    incident = get_incident(db, payload.incident_id)
    if incident is None:
        incident_data = {
            "id": payload.incident_id,
            "title": f"Incident {payload.incident_id}",
            "service_name": payload.service_name or "unknown-service",
            "severity": payload.severity or "medium",
            "summary": payload.signal_summary or "No summary available.",
        }
    else:
        incident_data = {
            "id": incident.id,
            "title": incident.title,
            "service_name": incident.service_name,
            "severity": incident.severity,
            "summary": incident.summary,
        }

    generated = generate_rca_from_model(incident_data)
    if incident is not None:
        save_rca_report(
            db,
            incident_id=incident_data["id"],
            provider=generated["provider"],
            model_name=generated["model_name"],
            probable_cause=generated["probable_cause"],
            executive_summary=generated["executive_summary"],
            remediation_steps=generated["remediation_steps"],
            confidence=generated["confidence"],
        )

    return RCAResponse(
        incident_id=incident_data["id"],
        provider=generated["provider"],
        model_name=generated["model_name"],
        probable_cause=generated["probable_cause"],
        confidence=generated["confidence"],
        remediation_steps=generated["remediation_steps"],
        executive_summary=generated["executive_summary"],
    )
