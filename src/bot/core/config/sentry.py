import logging

import sentry_sdk
from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings
from sentry_sdk.integrations.logging import LoggingIntegration

from bot.core.config.env import EnvironmentEnum

__all__ = [
    "SentrySettings",
    "init_sentry",
]


class SentrySettings(BaseSettings):
    dsn_url: str
    env_mode: EnvironmentEnum
    traces_sample_rate: float = Field(ge=0.0, le=1.0)

    class Config:
        env_prefix = "SENTRY_"


def init_sentry() -> None:
    logger.debug("Initializing Sentry")

    sentry_settings = SentrySettings()  # type: ignore[call-arg]

    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR,
    )

    sentry_sdk.init(
        dsn=sentry_settings.dsn_url,
        environment=sentry_settings.env_mode,
        traces_sample_rate=sentry_settings.traces_sample_rate,
        integrations=[sentry_logging],
        send_default_pii=True,
    )
