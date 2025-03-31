from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Дата", callback_data="opted_1"),
         InlineKeyboardButton(text="Сумма", callback_data="opted_2")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard