import logging

from core.config import config
from core.logging import setup_logging


logger = logging.getLogger(__name__)


def main():
    setup_logging()

    logger.debug("Hello World 1")
    logger.info("Hello World 2")
    logger.warning("Hello World 3")
    logger.error("Hello World 4")
    logger.critical("Hello World 5")
    logger.fatal("Hello World 6")
    logger.info(config.DEBUG)


if __name__ == "__main__":
    main()
