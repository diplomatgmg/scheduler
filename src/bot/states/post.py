from aiogram.fsm.state import State, StatesGroup


class PostState(StatesGroup):
    waiting_for_post = State()
