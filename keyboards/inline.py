from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder



main_menu_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Wallet", callback_data="wallet"),
        ],
    ])



wallet_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Пополнить", callback_data="deposit"),
            InlineKeyboardButton(text=f"Вывести", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton(text=f"Адресная книга", callback_data="address_book"),
        ],
        [
            InlineKeyboardButton(text=f"Коммисии и лимиты", callback_data="commissions_and_limits"),
        ],
        [
            InlineKeyboardButton(text=f"Назад", callback_data="main_menu"),
        ]
    ])

deposit_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Назад", callback_data="wallet"),
        ]
    ])

all_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Вывести все", callback_data="all"),
        ],

    ])
approve_cancel_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Подтвердить", callback_data="approve"),
            InlineKeyboardButton(text=f"Отменить", callback_data="cancel"),
        ],

    ])