from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold

from data.requests import add_user

from keyboards.inline import main_menu_ikb

router = Router()


@router.message(CommandStart())
@router.callback_query(F.data == "main_menu")
async def cmd_start(message: Message | CallbackQuery):
    await add_user(tg_chat_id=message.from_user.id, username=message.from_user.username)
    text = f"Hello, {hbold(message.from_user.full_name)}!"

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text, reply_markup=main_menu_ikb)
        await message.answer()
    else:
        await message.answer(text, reply_markup=main_menu_ikb)