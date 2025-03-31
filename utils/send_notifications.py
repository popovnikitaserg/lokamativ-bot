import asyncio
from aiogram import Bot, Dispatcher, Router, types
from create_bot import managers_id, admins, bot, managers_name
from db_handlers import db_func
from utils import image_maker


async def notify_daily():
    gen_text = "Нет оплат/предоплат по следующим заявкам:"
    gen_text_2 = "Нет окончательных оплат по следующим заявкам:"
    for id in managers_id:
        user_orders = await db_func.catch_orders_first_part(id)
        if len(user_orders) > 0:
            text = "Нет оплат/предоплат по следующим заявкам:"
            for order, sum in user_orders:
                text += f"\n07-{order}: {sum}"
                gen_text += f"\n07-{order}: {sum} ({managers_name[id]})"

            await bot.send_message(chat_id=id, text=text)

        user_orders_2 = await db_func.catch_orders_second_part(id)
        if len(user_orders_2) > 0:
            text = "Нет окончательных оплат по следующим заявкам:"
            for order, sum in user_orders_2:
                text += f"\n07-{order}: {sum}"
                gen_text_2 += f"\n07-{order}: {sum} ({managers_name[id]})"

            await bot.send_message(chat_id=id, text=text)

    for id in admins:
        if len(gen_text) > 41:
            await bot.send_message(chat_id=id, text=gen_text)
        if len(gen_text_2) > 45:
            await bot.send_message(chat_id=id, text=gen_text_2)
    return


async def notify_classification():
    await image_maker.best_managers()
    for id in managers_id:
        bot.send_photo(chat_id=id, photo="../statistics.png")
    for id in admins:
        await bot.send_photo(chat_id=id, photo=types.FSInputFile(path="../statistics.png"))