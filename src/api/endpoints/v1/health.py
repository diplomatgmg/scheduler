from fastapi import APIRouter

from api.endpoints.v1.schemas.health import HealthResponse


__all__ = [
    "router",
]


router = APIRouter()


@router.get("", status_code=200, summary="Проверка доступности сервера")
async def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
