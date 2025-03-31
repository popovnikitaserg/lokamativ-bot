import asyncio
import pandas as pd
from openpyxl.styles.builtins import calculation

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram import types
from selenium.webdriver.common.devtools.v132.console import clear_messages

from create_bot import managers_id
from db_handlers import db_func
from keyboards import for_options, for_edit_options
from utils import role_check

notify_router = Router()

class Form(StatesGroup):
    order_id = State()
    date = State()
    sum = State()

class Edit(StatesGroup):
    edit_num = State()
    edit_date = State()
    edit_sum = State()

global prefix
prefix = "07"

@notify_router.message(F.text == "Администрирование")
async def pick_option(message: Message, state: FSMContext):
    await state.clear()
    role = role_check.check(message.from_user.id)
    await message.answer("Выберите действие:", reply_markup=for_options.get_keyboard(role))


@notify_router.callback_query(F.data == "opt_1")
async def pick_number(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()

    await callback.message.answer(f"Укажите номер заявки (например, 07-100):")
    await state.set_state(Form.order_id)

@notify_router.callback_query(F.data == "opt_3")
async def return_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    role = role_check.check(callback.from_user.id)
    kb = [[types.KeyboardButton(text="Давайте рассчитаем.")]]
    if role == "admin":
        kb.append([types.KeyboardButton(text="Администрирование")])
    elif role == "manager":
        kb.append([types.KeyboardButton(text="Администрирование")])
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await callback.message.answer(f'Вы вернулись в главное меню. 🚢\nВыберите опцию:',
                         reply_markup=keyboard)

@notify_router.message(F.text.contains("07"), Form.order_id)
async def pick_date(message: Message, state: FSMContext):
    order_id = int(message.text.split("-")[1])
    result = await db_func.check_order(order_id)
    if result:
        await state.update_data(order_id=order_id)
        await message.answer(f"Укажите дату погрузки (например, 01-01-2025):")
        await state.set_state(Form.date)
    else:
        await message.answer(f"Заявка с номером {prefix}-{order_id} занята. Выберите другую.")
        await state.set_state(Form.order_id)


@notify_router.message(F.text, Form.date)
async def pick_sum(message: Message, state: FSMContext):
    await state.update_data(date=str(message.text))
    await message.answer(f"Укажите сумму заявки:")
    await state.set_state(Form.sum)

@notify_router.message(F.text, Form.sum)
async def save_order(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(sum=float(message.text))
    role = role_check.check(message.from_user.id)
    order_data = await state.get_data()
    order_data["user_id"] = int(message.from_user.id)
    result = await db_func.insert_order(order_data)
    if result:
        await message.answer(f"Заявка с номером {prefix}-{order_data["order_id"]} успешно сохранена! Выберите следующее действие:", reply_markup=for_options.get_keyboard(role))
        await state.clear()
        for id in managers_id:
            messg = await bot.send_message(chat_id=id, text=f"{prefix}-{order_data["order_id"]} занята.")
            await bot.unpin_chat_message(chat_id=messg.chat.id)
            await bot.pin_chat_message(chat_id=messg.chat.id, message_id=messg.message_id)

    else:
        await message.answer(f"Заявка с номером {prefix}-{order_data["order_id"]} занята. Выберите другую.")
        await state.clear()

@notify_router.callback_query(F.data == "opt_2")
async def pick_number_to_edit(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await callback.message.answer(f"Укажите номер заявки, которую нужно изменить (например, 07-100):")
    await state.set_state(Edit.edit_num)


@notify_router.message(F.text.contains("07"), Edit.edit_num)
async def edit_order(message: Message, state: FSMContext):
    role = role_check.check(message.from_user.id)
    if role == "manager" or role == "admin":
        order_id = int(message.text.split("-")[1])
        result = await db_func.check_order(order_id)
        await state.update_data(edit_num=order_id)
        if not result:
            await message.answer(f"Укажите, что вы хотите изменить:", reply_markup=for_edit_options.get_keyboard())
        else:
            await message.answer(f"Такой заявки нет. Укажите другой номер.")


@notify_router.callback_query(F.data == "opted_1")
async def edit_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await callback.message.answer(f"Укажите новую дату погрузки:")
    await state.set_state(Edit.edit_date)


@notify_router.message(F.text, Edit.edit_date)
async def edit_date(message: Message, state: FSMContext):
    role = role_check.check(message.from_user.id)
    if role == "manager" or role == "admin":
        await state.update_data(edit_date=str(message.text))
        update_data = await state.get_data()
        result = await db_func.update_date(update_data)
        if result:
            await message.answer(f"Изменения внесены!\nВыберите следующее действие", reply_markup=for_options.get_keyboard(role))
            await state.clear()
        else:
            await message.answer(f"Формат данных неверен.")

@notify_router.callback_query(F.data == "opted_2")
async def edit_date(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await callback.message.answer(f"Укажите новую сумму:")
    await state.set_state(Edit.edit_sum)

@notify_router.message(F.text, Edit.edit_sum)
async def edit_date(message: Message, state: FSMContext):
    role = role_check.check(message.from_user.id)
    if role == "manager" or role == "admin":
        await state.update_data(edit_sum=float(message.text))
        update_data = await state.get_data()
        result = await db_func.update_sum(update_data)
        if result:
            await message.answer(f"Изменения внесены!\nВыберите следующее действие", reply_markup=for_options.get_keyboard(role))
            await state.clear()
        else:
            await message.answer(f"Формат данных неверен.")

@notify_router.callback_query(F.data == "opt_4")
async def pick_number_to_edit(callback: types.CallbackQuery, state:FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()
    await callback.message.answer(f"Отправьте файл Excel.")

@notify_router.message(F.document)
async def handle_excel(message: Message):
    role = role_check.check(message.from_user.id)
    if role == "admin":
        if message.document.mime_type not in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                              "application/vnd.ms-excel"]:
            await message.answer("Файл отправлен не в том формате.")
            return
        file_id = message.document.file_id
        file_info= await message.bot.get_file(file_id)
        file = await message.bot.download_file(file_info.file_path)
        with open('data.xlsx', 'wb') as f:
            f.write(file.read())

        df = pd.read_excel('data.xlsx')

        result = await db_func.process_excel_data(df)
        if result:
            await message.answer("Оплаты внесены", reply_markup=for_options.get_keyboard(role))
        else:
            await message.answer("В файле указаны несуществующие номера заказов")
    else:
        "У вас нет полномочий."