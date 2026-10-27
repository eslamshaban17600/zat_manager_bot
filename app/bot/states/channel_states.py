from aiogram.fsm.state import State, StatesGroup

class ChannelAddStates(StatesGroup):
    waiting_for_channel_input = State()