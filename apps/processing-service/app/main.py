from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.workers.consumer import TelemetryConsumer
from opsyra_common.config import get_shared_settings
from opsyra_common.database import init_database

tags_metadata = [
    {
        "name": "health",
        "description": "Basic service readiness checks for local development and orchestration.",
    },
    {
        "name": "processing",
        "description": "Endpoints for anomaly detection and telemetry enrichment workflows.",
    },
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    shared_settings = get_shared_settings()
    consumer = None
    if shared_settings.processing_enable_consumer:
        consumer = TelemetryConsumer()
        consumer.start()
    yield
    if consumer is not None:
        consumer.stop()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Processes telemetry and produces anomaly insights.",
    lifespan=lifespan,
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
        "message": "Opsyra processing service is running.",
        "docs": settings.docs_url,
        "openapi": settings.openapi_url,
    }
