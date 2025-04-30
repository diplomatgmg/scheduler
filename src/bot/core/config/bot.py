from pydantic_settings import BaseSettings

__all__ = [
    "BotConfig",
]


class BotConfig(BaseSettings):
    token: str
    support_username: str

    class Config:
        env_prefix = "BOT_"
