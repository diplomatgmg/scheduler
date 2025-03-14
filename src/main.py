import logging

from core import config
from core.logging import setup_logger

logger = logging.getLogger(__name__)


def main():
    setup_logger()

    logger.debug("Hello World 1")
    logger.info("Hello World 2")
    logger.warning("Hello World 3")
    logger.error("Hello World 4")
    logger.critical("Hello World 5")
    logger.info(config.DEBUG)


if __name__ == "__main__":
    main()
