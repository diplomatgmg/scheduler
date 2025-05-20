from pydantic import BaseModel


__all__ = [
    "RootResponse",
]


class RootResponse(BaseModel):
    docs: str
