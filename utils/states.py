from aiogram.fsm.state import StatesGroup, State


class WithdrawForm(StatesGroup):
    address = State()
    amount = State()
    approve = State()

    withdraw_fee = State()
    allin = State()
