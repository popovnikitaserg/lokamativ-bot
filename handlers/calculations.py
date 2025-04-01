import asyncio
import random

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import re
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram import types
from keyboards import for_quantity, for_restart, for_destinations, for_manager
from utils import price_calculator, format_checker

from utils import price_calculator

from create_bot import destinations, managers

class Form(StatesGroup):
    destination = State()
    quantity = State()
    dimensions = State()
    weight = State()

capture_router = Router()

@capture_router.message(F.text == "Давайте рассчитаем.")
async def pick_destination(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📍Выберите направление перевозки:",
                         reply_markup=for_destinations.get_keyboard())
    await state.set_state(Form.destination)


@capture_router.callback_query(F.data.startswith("dest_"), Form.destination)
async def pick_quantity(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    dest_id = int(callback.data.replace('dest_', ''))
    dest_data = destinations[dest_id]["dest"]
    await state.update_data(destination=dest_data)
    await callback.message.answer(f"📍✅ Вы выбрали направление:\n<b>{dest_data}</b>")
    await bot.send_message(chat_id=callback.message.chat.id,
                           text="🎲 Выберите количество грузовых мест либо укажите число:",
                           reply_markup=for_quantity.get_keyboard())
    await state.set_state(Form.quantity)

@capture_router.callback_query(F.data.startswith("num_"), Form.quantity)
async def callbacks_num(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    button = callback.data.split("_")[1]
    if button == "more":
        await callback.message.answer("Укажите число:")
    else:
        await state.update_data(quantity=int(button))
        await callback.message.answer(f"🎲 ✅ Вы выбрали количество мест: <b>{button}</b>")
        await bot.send_message(chat_id=callback.message.chat.id,
                               text="📦 Теперь давайте укажем габариты каждого грузового места.\n\nУказывайте габариты в <u>сантиметрах</u> (см) в формате:\n<b>ДхШхВ</b>\n<blockquote>Пример: 100х100х100</blockquote>\n\nЕсли грузов больше, чем один, каждый <u>размер пишите с новой строки</u>.\n<blockquote>Пример:\n100х100х100\n100х100х100\n100х100х100</blockquote>",
                               reply_markup=for_restart.get_keyboard())
        await state.set_state(Form.dimensions)

@capture_router.message(Form.quantity, lambda message: (message.text.isalpha() and message.text != None))
async def wrong_format(message: Message, state: FSMContext, bot: Bot):
    await message.answer("❌ Вы неправильно указали количество грузовых мест.\nПопробуйте ещё раз!", reply_markup=for_restart.get_keyboard())

@capture_router.message(Form.quantity, lambda message: message.text.isdigit())
async def start_calculation(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(quantity=int(message.text))
    await message.answer(f"🎲 ✅ Вы выбрали количество мест: <b>{message.text}</b>")
    await bot.send_message(chat_id=message.chat.id,
                           text="📦 Теперь давайте укажем габариты каждого грузового места.\n\nУказывайте габариты в <u>сантиметрах</u> (см) в формате:\n<b>ДхШхВ</b>\n<blockquote>Пример: 100х100х100</blockquote>\n\nЕсли грузов больше, чем один, каждый <u>размер пишите с новой строки</u>.\n<blockquote>Пример:\n100х100х100\n100х100х100\n100х100х100</blockquote>",
                         reply_markup=for_restart.get_keyboard())
    await state.set_state(Form.dimensions)


@capture_router.message(F.text != "🔄 Начать рассчет заново!", Form.dimensions)
async def start_calculation(message: Message, state: FSMContext, bot: Bot):
    msg = message.text
    quantity = await state.get_data()
    quantity = quantity.get("quantity")
    splitted = re.split(r"[-;,.\s\n]\s*", msg)
    splitted = [s.strip() for s in splitted]
    if len(splitted) != quantity:
        await message.reply("❌ Вы указали габариты не всех грузовых мест.\nПопробуйте ещё раз!", reply_markup=for_restart.get_keyboard())
        await state.set_state(Form.dimensions)
    else:
        if format_checker.check_dimensions(splitted):
            await state.update_data(dimensions=splitted)
            text = "📦 ✅ Размеры Ваших грузов следующие:\n\n"
            for i, dim in enumerate(splitted):
                text += f"<b>{i + 1}. {dim} см</b>\n"
            messg = await message.answer(text)
            await bot.send_message(chat_id=messg.chat.id, text="🪝 Осталось указать только вес каждого грузового места.\n\nНапишите вес каждого груза в <u>килограммах</u> (кг).\n<blockquote>Пример: 100</blockquote>\n\nЕсли грузов больше, чем один, каждый <u>вес пишите с новой строки</u>.\n<blockquote>Пример:\n100\n250\n300</blockquote>", reply_markup=for_restart.get_keyboard())
            await state.set_state(Form.weight)
        else:
            await message.answer("🙁 Вы указали габариты в неправильном формате.\nПопробуйте ещё раз.", reply_markup=for_restart.get_keyboard())
            await state.set_state(Form.dimensions)


@capture_router.message(F.text != "🔄 Начать рассчет заново!", Form.weight)
async def start_calculation(message: Message, state: FSMContext, bot: Bot):
    msg = message.text
    quantity = await state.get_data()
    quantity = quantity.get("quantity")
    splitted = re.split(r"[-;,.\s]\s*", msg)
    splitted = [s.strip() for s in splitted]
    if len(splitted) != quantity:
        await message.reply("❌ Вы указали веса не всех грузовых мест.\nПопробуйте ещё раз!", reply_markup=for_restart.get_keyboard())
        await state.set_state(Form.weight)
    else:
        if format_checker.check_weights(splitted):
            await state.update_data(weight=splitted)
            text = "🪝✅ Вес каждого Вашего грузового места следующий:\n\n"
            for i, weight in enumerate(splitted):
                text += f"<b>{i + 1}. {weight} кг</b>\n"
            messg = await message.answer(text)
            data = await state.get_data()

            quantity = data.get('quantity')
            dimensions = data.get('dimensions')
            weights = data.get('weight')

            price = price_calculator.calculate(quantity, dimensions, weights)


            new_msg = await bot.send_message(messg.chat.id,"Отлично!\n\n💰Ориентировочная стоимость перевозки:\n"
                                 f"<u>{price:.0f}</u>", reply_markup=for_restart.get_keyboard())
            await state.clear()
            await asyncio.sleep(3)
            await bot.send_message(chat_id=new_msg.chat.id, text="👩🏼‍💼 Хотите связаться с менеджером для уточнения деталей?", reply_markup=for_manager.get_keyboard())

        else:
            await message.answer("🙁 Вы указали веса в неправильном формате.\nПопробуйте ещё раз.", reply_markup=for_restart.get_keyboard())
            await state.set_state(Form.weight)


@capture_router.callback_query(F.data.startswith("ans_"))
async def need_manager(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer()
    button = call.data.split("_")[1]
    if button == "1":
        name, phone = random.choice(managers)
        await call.message.answer(f"Отличный выбор!\n\n☎️ Вот номер для связи с нашим менеджером:\n{phone}, {name}")
    else:
        await call.message.answer(f"До скорых встреч!\nДля пересчёта нажмите на кнопку <b>Начать рассчёт заново!</b>")



@capture_router.message(F.text == "🔄 Начать рассчет заново!")
async def restart_calculation(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📍Выберите направление перевозки:",
                         reply_markup=for_destinations.get_keyboard())
    await state.set_state(Form.destination)
