from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    buttons = [
        [InlineKeyboardButton(text="✅ Да", callback_data="ans_1")],
        [InlineKeyboardButton(text="❌ Нет", callback_data="ans_2")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard