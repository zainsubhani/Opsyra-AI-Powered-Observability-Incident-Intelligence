from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings

tags_metadata = [
    {
        "name": "health",
        "description": "Basic service readiness checks for local development and orchestration.",
    },
    {
        "name": "query",
        "description": "Read-only APIs used by dashboards, incident views, and service health panels.",
    },
]


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Serves incidents, services, and observability query APIs.",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
    openapi_tags=tags_metadata,
    swagger_ui_parameters={"defaultModelsExpandDepth": 1, "displayRequestDuration": True},
)
app.include_router(api_router, prefix="/api/v1")


@app.get("/healthz", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_slug}


@app.get("/", tags=["health"], summary="Service entrypoint")
def root() -> dict[str, str]:
    return {
        "message": "Opsyra query service is running.",
        "docs": settings.docs_url,
        "openapi": settings.openapi_url,
    }
