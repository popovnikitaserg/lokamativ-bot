from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="1", callback_data="num_1"),
            InlineKeyboardButton(text="2", callback_data="num_2"),
            InlineKeyboardButton(text="3", callback_data="num_3"),
            InlineKeyboardButton(text="4", callback_data="num_4"),
            InlineKeyboardButton(text="5", callback_data="num_5")
        ],
        [InlineKeyboardButton(text="Более", callback_data="num_more")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard