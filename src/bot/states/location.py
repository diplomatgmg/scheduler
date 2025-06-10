from aiogram.fsm.state import State, StatesGroup


__all__ = ["LocationState"]


class LocationState(StatesGroup):
    waiting_for_method = State()

    waiting_for_share = State()
    waiting_for_manual_choose = State()
