from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard():
    kb = [[KeyboardButton(text="🔄 Начать рассчет заново!")]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard