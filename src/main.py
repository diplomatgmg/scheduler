from core.logging import setup_logging
import logging

logger = logging.getLogger(__name__)


def main():
    logger.debug("Hello World 10")
    logger.info("Hello World 2")
    logger.warning("Hello World 3")
    logger.error("Hello World 4")
    logger.critical("Hello World 5")
    logger.fatal("Hello World 5")


if __name__ == "__main__":
    setup_logging()
    main()
