from aiogram import Router, types
from aiogram.filters import CommandStart
from create_bot import admins, managers_id

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    kb = [[types.KeyboardButton(text="Давайте рассчитаем.")]]
    if message.from_user.id in admins:
        kb.append([types.KeyboardButton(text="Администрирование")])
    if message.from_user.id in managers_id:
        kb.append([types.KeyboardButton(text="Администрирование")])
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer(f'Здравствуйте, это бот для расчёта стоимости перевозки. 🚢\nВыберите опцию:', reply_markup=keyboard)
