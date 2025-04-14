from pydantic_settings import BaseSettings

__all__ = [
    "BotSettings",
]


class BotSettings(BaseSettings):
    token: str
    support_username: str

    class Config:
        env_prefix = "BOT_"
