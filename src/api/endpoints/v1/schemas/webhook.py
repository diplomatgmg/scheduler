from typing import Literal

from pydantic import BaseModel


__all__ = [
    "WebhookResponse",
]


class WebhookResponse(BaseModel):
    status: Literal["ok"] = "ok"
