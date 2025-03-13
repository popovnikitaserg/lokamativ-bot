from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [[types.KeyboardButton(text="Давайте рассчитаем.")]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer(f'Здравствуйте,\nДавайте рассчитаем стоимость перевозки ваших грузов.', reply_markup=keyboard)
