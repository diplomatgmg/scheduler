from aiogram.fsm.state import State, StatesGroup


__all__ = ["PostCreateState"]


class PostCreateState(StatesGroup):
    channel_selection = State()
    process_post = State()
    process_buttons = State()
    process_publish = State()
