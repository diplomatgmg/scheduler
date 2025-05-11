from pydantic import BaseModel


__all__ = [
    "HealthResponse",
]


class HealthResponse(BaseModel):
    status: str
