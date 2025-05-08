from fastapi import APIRouter

from api.endpoints.v1.health import router as health_router


__all__ = ["router"]


router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
