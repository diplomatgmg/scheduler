from aiogram.fsm.state import State, StatesGroup


__all__ = [
    "PostCreateState",
    "PostScheduleState",
]


class PostCreateState(StatesGroup):
    waiting_for_channel = State()
    waiting_for_post = State()
    waiting_for_buttons = State()


class PostScheduleState(StatesGroup):
    waiting_for_publish = State()
    waiting_for_schedule = State()
    waiting_for_delete_timer = State()
