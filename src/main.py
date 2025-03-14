import logging

import uvloop

from core import config
from core.logging import setup_logger
from handlers import get_handlers_router
from loader import bot, dp

logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logger()
    logger.info("Режим разработки - %s", config.ENVIRONMENT.value)

    dp.include_router(get_handlers_router())

    await dp.start_polling(bot)


if __name__ == "__main__":
    uvloop.run(main())
