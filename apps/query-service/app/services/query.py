from app.schemas.query import (
    IncidentItem,
    IncidentListResponse,
    ServiceOverviewItem,
    ServiceOverviewResponse,
)


def list_incidents() -> IncidentListResponse:
    incidents = [
        IncidentItem(
            incident_id="inc_1001",
            service_name="payments-service",
            severity="critical",
            status="investigating",
            title="Payment API latency spike",
        ),
        IncidentItem(
            incident_id="inc_1002",
            service_name="checkout-service",
            severity="medium",
            status="open",
            title="Elevated checkout error rate",
        ),
    ]
    return IncidentListResponse(incidents=incidents, total=len(incidents))


def service_overview() -> ServiceOverviewResponse:
    services = [
        ServiceOverviewItem(
            service_name="payments-service",
            health="degraded",
            open_incidents=1,
            p95_latency_ms=480,
            error_rate_percent=3.1,
        ),
        ServiceOverviewItem(
            service_name="checkout-service",
            health="healthy",
            open_incidents=1,
            p95_latency_ms=190,
            error_rate_percent=0.8,
        ),
    ]
    return ServiceOverviewResponse(services=services, generated_from="sample-observability-store")
