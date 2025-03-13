from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Склад Санкт-Петербург - Склад Калининград", callback_data="dest_1")],
        [InlineKeyboardButton(text="Склад Калининград - Склад Санкт-Петербург", callback_data="dest_2")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard