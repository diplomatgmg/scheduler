from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings


__all__ = [
    "sentry_config",
]


class SentryConfig(BaseSettings):
    dsn_url: HttpUrl
    traces_sample_rate: float = Field(ge=0.0, le=1.0)

    class Config:
        env_prefix = "SENTRY_"


sentry_config = SentryConfig()
