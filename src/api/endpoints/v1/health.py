from fastapi import APIRouter


__all__ = ["router"]


router = APIRouter()


@router.get("/", status_code=204, summary="Проверка доступности сервера")
async def health_check() -> None:
    return None
