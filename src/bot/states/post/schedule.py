from aiogram.fsm.state import State, StatesGroup


__all__ = ["PostScheduleState"]


class PostScheduleState(StatesGroup):
    waiting_for_publish = State()
    waiting_for_schedule = State()
    waiting_for_delete_timer = State()
