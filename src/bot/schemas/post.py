from pydantic import BaseModel

__all__ = [
    "PostContext",
]


class PostContext(BaseModel):
    selected_channel_title: str
    selected_channel_username: str | None
