from aiogram.fsm.state import State, StatesGroup


__all__ = ["TimezoneSetupState"]


class TimezoneSetupState(StatesGroup):
    waiting_for_timezone = State()
    manual_selection = State()
