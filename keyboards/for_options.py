from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard(role):
    if role == "manager":
        buttons = [
            [InlineKeyboardButton(text="Занять номер заявки", callback_data="opt_1"),
             InlineKeyboardButton(text="Внести изменения", callback_data="opt_2")],
            [InlineKeyboardButton(text="В главное меню", callback_data="opt_3")],
        ]
    elif role == "admin":
        buttons = [
            [InlineKeyboardButton(text="Занять номер заявки", callback_data="opt_1"),
             InlineKeyboardButton(text="Внести изменения", callback_data="opt_2")],
            [InlineKeyboardButton(text="Внести оплаты", callback_data="opt_4")],
            [InlineKeyboardButton(text="В главное меню", callback_data="opt_3")],
        ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard