from aiogram.fsm.state import State, StatesGroup

class InstantPostStates(StatesGroup):
    waiting_for_channel_selection = State()
    waiting_for_post_content = State()
    waiting_for_confirmation = State()