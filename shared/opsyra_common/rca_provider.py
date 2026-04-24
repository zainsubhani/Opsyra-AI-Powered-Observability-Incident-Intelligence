from __future__ import annotations

from typing import Any

import httpx

from opsyra_common.config import get_shared_settings


def _fallback_rca(incident: dict[str, Any]) -> dict[str, Any]:
    probable_cause = (
        f"The incident is most likely linked to instability in {incident['service_name']} "
        f"after telemetry showed {incident['summary'].lower()}."
    )
    return {
        "provider": "heuristic",
        "model_name": "rule-based",
        "probable_cause": probable_cause,
        "executive_summary": (
            f"{incident['title']} is affecting {incident['service_name']} with "
            f"{incident['severity']} severity and needs operator attention."
        ),
        "remediation_steps": [
            f"Inspect the most recent deploys and config changes for {incident['service_name']}.",
            "Review database, cache, and downstream dependency saturation.",
            "Roll back the highest-risk change if the incident is still expanding.",
        ],
        "confidence": 0.58,
    }


def generate_rca_from_model(incident: dict[str, Any]) -> dict[str, Any]:
    settings = get_shared_settings()
    if not settings.openai_api_key:
        return _fallback_rca(incident)

    prompt = (
        "You are an SRE assistant. Return concise JSON with keys "
        "probable_cause, executive_summary, remediation_steps, confidence. "
        f"Incident title: {incident['title']}. "
        f"Service: {incident['service_name']}. "
        f"Severity: {incident['severity']}. "
        f"Summary: {incident['summary']}."
    )
    try:
        with httpx.Client(timeout=20.0) as client:
            response = client.post(
                f"{settings.openai_base_url.rstrip('/')}/responses",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.openai_model,
                    "instructions": "Return only valid JSON.",
                    "input": prompt,
                },
            )
            response.raise_for_status()
            payload = response.json()
            content = payload["output"][0]["content"][0]["text"]
    except Exception:
        return _fallback_rca(incident)

    import json

    try:
        parsed = json.loads(content)
        return {
            "provider": "openai",
            "model_name": settings.openai_model,
            "probable_cause": parsed["probable_cause"],
            "executive_summary": parsed["executive_summary"],
            "remediation_steps": parsed["remediation_steps"],
            "confidence": float(parsed["confidence"]),
        }
    except Exception:
        return _fallback_rca(incident)
