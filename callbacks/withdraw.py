import re

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config_reader import config
from data.requests import get_user_balance_monero, withdraw_send_to_wallet_monero

from filters.is_digit_or_float import is_valid_monero_address, CheckForDigit
from keyboards.inline import approve_cancel_ikb, all_ikb, deposit_ikb

from utils.states import WithdrawForm

router = Router()


@router.callback_query(F.data == "withdraw")
async def form_withdraw(call: CallbackQuery, state: FSMContext):
    await state.set_state(WithdrawForm.address)
    await call.message.edit_text(
        "Введите адрес Monero в сети Monero:"
    )


@router.message(WithdrawForm.address)
async def form_address(message: Message, state: FSMContext):
    if is_valid_monero_address(message.text):
        balance = await get_user_balance_monero(message.from_user.id)
        print("Строка соответствует регулярному выражению.")
        await state.update_data(address=message.text)
        await state.set_state(WithdrawForm.amount)
        await message.answer(f"Ваш текущий баланс: <code>{balance}</code> XMR\n"
                             f"Адрес куда: <code>{message.text}</code>\n"
                             f"\n"
                             f"Введите сумму вывода:", reply_markup=all_ikb)
    else:
        print("Строка не соответствует регулярному выражению.")
        await message.answer(f"Ошибочка, вы ввели не корректный адрес...\n"
                             f"\n"
                             f"Введите адрес Monero в сети Monero:")


@router.message(WithdrawForm.amount, CheckForDigit())
@router.callback_query(F.data == "all")
async def form_amount(message: Message | CallbackQuery, state: FSMContext):
    withdraw_fee = config.monero_withdraw_fee
    await state.update_data(withdraw_fee=withdraw_fee)
    data = await state.get_data()


    balance = await get_user_balance_monero(message.from_user.id)
    if isinstance(message, Message):
        await state.update_data(allin=False)
        user_amount = float(message.text)
        total_amount = user_amount + withdraw_fee
        if balance > total_amount:
            print(data['address'])
            print("Строка соответствует регулярному выражению.")
            await state.update_data(amount=user_amount)
            await message.answer(f"Адрес куда: <code>{data['address']}</code>\n"
                                 f"Сумма <code>{message.text}</code>\n"
                                 f"\n"
                                 f"Коммисия сервиса: <code>{withdraw_fee}</code>\n"
                                 f"Подтвердить перевод ?",
                                 reply_markup=approve_cancel_ikb)
            await state.set_state(WithdrawForm.approve)
        else:
            await message.answer(f"Не достаточно средств\n"
                                 f"Ваш текущий баланс: <code>{balance}</code>\n"
                                 f"Комиссия: <code>{withdraw_fee}</code>\n"
                                 f"Максимум на вывод: <code>{balance - withdraw_fee}</code>\n"
                                 f"\n"
                                 f"Введите сумму на вывод:")

    else:
        total_amount = balance - withdraw_fee
        if balance > total_amount:
            await state.update_data(amount=balance)
            await state.update_data(allin=True)
            await message.edit(f"Адрес куда: <code>{data['address']}</code>\n"
                                 f"Сумма <code>{total_amount}</code>\n"
                                 f"\n"
                                 f"Коммисия сервиса: <code>{withdraw_fee}</code>"
                                 f"Подтвердить перевод ?",
                                 reply_markup=approve_cancel_ikb)
            await state.set_state(WithdrawForm.approve)
        else:
            await message.answer(f"Не достаточно средств\n"
                                 f"Ваш текущий баланс: <code>{balance}</code>\n"
                                 f"Комиссия: <code>{withdraw_fee}</code>\n"
                                 f"Максимум на вывод: <code>{balance - withdraw_fee}</code>\n"
                                 f"\n"
                                 f"Введите сумму на вывод:")


@router.callback_query(WithdrawForm.approve)
async def form_approve(call: CallbackQuery, state: FSMContext):
    if call.data == "approve":
        print("Транзакция отправляется")

        data = await state.get_data()
        txid = await withdraw_send_to_wallet_monero(service_transfer_fee=data["withdraw_fee"],to_address=data["address"],
                                                    amount=data["amount"],
                                                    allin=data["allin"],
                                                    tg_chat_id=call.from_user.id)
        await state.clear()
        if txid:
            await call.message.answer(f"Транзакция успешно отправлена\n"
                                      f"TXID: <code>{txid}</code>\n",
                                      reply_markup=deposit_ikb)
        else:
            await call.message.answer(f"Произошла ошибка\n")
    elif call.data == "cancel":
        print("Транзакция отменена")
        await call.message.answer(f"Транзакция отменена\n",
                                  reply_markup=deposit_ikb)
        await state.clear()
    else:
        print("хз что там еще может быть но мне так нравится")
