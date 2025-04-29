from aiogram.fsm.state import State, StatesGroup

__all__ = [
    "PostState",
]


class PostState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_text = State()  # FIXME unused
    waiting_for_post = State()  # FIXME он же waiting_for_text?
