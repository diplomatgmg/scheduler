from fastapi import APIRouter

from api.endpoints.v1.health import router as health_router
from api.endpoints.v1.webhook import router as webhook_router


__all__ = [
    "router",
]


router = APIRouter()

router.include_router(health_router, prefix="/health", tags=["health"])
router.include_router(webhook_router, prefix="/webhook", tags=["webhook"])
