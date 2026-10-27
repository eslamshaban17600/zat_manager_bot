from aiogram.fsm.state import State, StatesGroup

class TransferOwnershipStates(StatesGroup):
    waiting_for_new_owner_id = State()
    waiting_for_confirmation = State()