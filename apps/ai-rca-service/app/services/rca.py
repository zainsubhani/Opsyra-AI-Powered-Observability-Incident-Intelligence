from app.schemas.rca import RCARequest, RCAResponse


def generate_rca(payload: RCARequest) -> RCAResponse:
    probable_cause = (
        f"The most likely cause is instability in {payload.suspected_component} "
        f"affecting {payload.service_name} during the incident window."
    )
    remediation_steps = [
        f"Inspect recent deploys and config changes for {payload.suspected_component}.",
        f"Check dependency health and saturation metrics for {payload.service_name}.",
        "Roll back the last risky change if the error budget is still burning.",
    ]
    executive_summary = (
        f"Incident {payload.incident_id} appears tied to {payload.suspected_component}. "
        f"Observed signals suggest a {payload.severity} severity service degradation."
    )

    return RCAResponse(
        incident_id=payload.incident_id,
        probable_cause=probable_cause,
        confidence=0.82,
        remediation_steps=remediation_steps,
        executive_summary=executive_summary,
    )
