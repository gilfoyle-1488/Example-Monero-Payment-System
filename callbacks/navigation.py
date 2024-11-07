from aiogram import Router, F
from aiogram.types import CallbackQuery
from data.requests import get_user_balance_monero, get_address_monero
from keyboards.inline import wallet_ikb, deposit_ikb

router = Router()


@router.callback_query(F.data == "wallet")
async def wallet(call: CallbackQuery):
    balance_monero = await get_user_balance_monero(call.from_user.id)
    print(balance_monero)
    await call.message.edit_text(f"Ваш баланс: <code>{balance_monero}</code> XMR", reply_markup=wallet_ikb)


@router.callback_query(F.data == "deposit")
async def deposit(call: CallbackQuery):
    address = await get_address_monero(call.from_user.id)
    await call.message.edit_text(f"Ваш address: <code>{address}</code> XMR", reply_markup=deposit_ikb)
