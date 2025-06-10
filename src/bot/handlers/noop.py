from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot.callbacks.noop import NoopActionEnum, NoopCallback


__all__ = ["router"]


router = Router(name="noop")


# noinspection PyTypeChecker
@router.callback_query(NoopCallback.filter(F.action == NoopActionEnum.DO_NOTHING))
async def handle_noop_callback(query: CallbackQuery) -> None:
    await query.answer("Ничего не произошло")
