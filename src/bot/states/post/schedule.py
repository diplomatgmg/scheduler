from aiogram.fsm.state import State, StatesGroup


__all__ = ["PostScheduleState"]


class PostScheduleState(StatesGroup):
    waiting_for_publish = State()

    waiting_for_schedule = State()
    waiting_for_date = State()
    waiting_for_time = State()

    waiting_for_delete_timer = State()
