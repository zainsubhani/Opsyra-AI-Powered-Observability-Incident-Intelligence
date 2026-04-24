import json
import re
import threading
from datetime import datetime, timezone

from sqlalchemy import func, select

from opsyra_common.config import get_shared_settings
from opsyra_common.database import SessionLocal
from opsyra_common.models import IncidentRecord
from opsyra_common.queue import get_redis_client
from opsyra_common.repository import create_incident, mark_telemetry_processed, upsert_service_snapshot


LATENCY_PATTERN = re.compile(r"(\d+)\s*ms", re.IGNORECASE)


def _infer_incident(message: str, severity: str) -> bool:
    lowered = message.lower()
    return severity in {"error", "critical"} or any(
        token in lowered for token in ("timeout", "failed", "latency", "error", "exception")
    )


def _infer_latency(message: str) -> int:
    match = LATENCY_PATTERN.search(message)
    if match:
        return int(match.group(1))
    return 450 if "latency" in message.lower() else 0


def _infer_error_rate(severity: str) -> float:
    if severity == "critical":
        return 9.7
    if severity == "error":
        return 4.1
    if severity == "warning":
        return 1.6
    return 0.4


class TelemetryConsumer:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def _run(self) -> None:
        settings = get_shared_settings()
        client = get_redis_client()
        if client is None:
            return

        last_id = "0-0"
        while not self._stop.is_set():
            result = client.xread(
                {settings.telemetry_stream_name: last_id},
                block=settings.processing_stream_block_ms,
                count=10,
            )
            if not result:
                continue

            for _, entries in result:
                for stream_id, entry in entries:
                    payload = json.loads(entry["payload"])
                    self._process_payload(payload)
                    last_id = stream_id

    def _process_payload(self, payload: dict[str, str]) -> None:
        db = SessionLocal()
        try:
            severity = payload["severity"]
            message = payload["message"]
            service_name = payload["service_name"]

            if _infer_incident(message, severity):
                create_incident(
                    db,
                    service_name=service_name,
                    severity="critical" if severity == "critical" else "high",
                    title=f"{service_name} incident detected",
                    summary=message,
                    source_event_id=payload["event_id"],
                )

            open_incidents = db.scalar(
                select(func.count())
                .select_from(IncidentRecord)
                .where(
                    IncidentRecord.service_name == service_name,
                    IncidentRecord.status == "open",
                )
            )
            health = "healthy"
            if open_incidents:
                health = "down" if severity == "critical" else "degraded"

            upsert_service_snapshot(
                db,
                service_name=service_name,
                health=health,
                open_incidents=int(open_incidents or 0),
                p95_latency_ms=_infer_latency(message),
                error_rate_percent=_infer_error_rate(severity),
                last_summary=message,
            )
            mark_telemetry_processed(db, payload["event_id"])
        finally:
            db.close()
