from fastapi import APIRouter

from app.api.v1.processing import router as processing_router


api_router = APIRouter()
api_router.include_router(processing_router, prefix="/processing", tags=["processing"])
