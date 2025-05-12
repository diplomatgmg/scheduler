import logging

from loguru import logger
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from common.environment.config import env_config
from common.sentry.config import sentry_config


__all__ = [
    "setup_sentry",
]


def setup_sentry() -> None:
    if sentry_config.enabled:
        logger.debug("Skip initializing Sentry")
        return

    logger.debug("Initializing Sentry")

    sentry_logging = LoggingIntegration(
        level=logging.WARNING,
        event_level=logging.ERROR,
    )

    sentry_sdk.init(
        dsn=str(sentry_config.dsn_url),
        environment=env_config.mode,
        traces_sample_rate=sentry_config.traces_sample_rate,
        integrations=[sentry_logging],
        send_default_pii=True,
    )
