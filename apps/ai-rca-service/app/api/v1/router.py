from fastapi import APIRouter

from app.api.v1.rca import router as rca_router


api_router = APIRouter()
api_router.include_router(rca_router, prefix="/rca", tags=["rca"])
