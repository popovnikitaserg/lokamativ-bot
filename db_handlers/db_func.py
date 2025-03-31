import asyncio
from datetime import datetime, date, timedelta

import pandas as pd

from sqlalchemy import func
from create_bot import AsyncSessionLocal
from db_handlers.models import Order
from sqlalchemy.future import select
from create_bot import engine, Base

async def insert_order(order_data):
    async with AsyncSessionLocal() as session:
        # Convert "DD-MM-YYYY" string to a date object
        date = datetime.strptime(order_data["date"], "%d-%m-%Y").date()

        new_order = Order(order_id=order_data["order_id"],user_id=order_data["user_id"], date=date, sum=order_data["sum"])
        session.add(new_order)
        await session.commit()
        return True

async def check_order(order_id):
    async with AsyncSessionLocal() as session:
        existing_order = await session.execute(select(Order).where(Order.order_id == order_id))
        if existing_order.scalar():
            return False
        return True


async def update_date(update_data):
    async with AsyncSessionLocal() as session:
        order = await session.get(Order, update_data["edit_num"])
        if not order:
            return False
        order.date = datetime.strptime(update_data["edit_date"], "%d-%m-%Y").date()
        await session.commit()
        return True

async def update_sum(update_data):
    async with AsyncSessionLocal() as session:
        order = await session.get(Order, update_data["edit_num"])
        if not order:
            return False
        order.sum = update_data["edit_sum"]
        await session.commit()
        return True

async def process_excel_data(df: pd.DataFrame):
    required_columns = ['Номер', 'Сумма']

    # Check if required columns exist
    if not all(col in df.columns for col in required_columns):
        return False

    # Iterate through the rows and insert data into the database
    async with AsyncSessionLocal() as session:
        for _, row in df.iterrows():
            order_id = int(row['Номер'])
            sum_amount = float(row['Сумма'])

            order = await session.get(Order, order_id)
            if not order:
                return False
            order.sum -= sum_amount

        await session.commit()
    return True

async def catch_orders_first_part(user_id):
    async with AsyncSessionLocal() as session:
        today = date.today()  # Получаем сегодняшнюю дату
        date_limit = today - timedelta(days=1)

        async with session.begin():
            result = await session.execute(
                select(Order.order_id, Order.sum)
                .where(Order.user_id == user_id, Order.sum > 0, Order.date == date_limit)
            )
            orders = result.all()

    return [(order_id, sum_amount) for order_id, sum_amount in orders]

async def catch_orders_second_part(user_id):
    async with AsyncSessionLocal() as session:
        today = date.today()  # Получаем сегодняшнюю дату
        date_limit = today - timedelta(days=14)  # Вычисляем границу по дате

        async with session.begin():
            result = await session.execute(
                select(Order.order_id, Order.sum)
                .where(Order.user_id == user_id, Order.sum > 0, Order.date <= date_limit)
            )
            orders = result.all()

    return [(order_id, sum_amount) for order_id, sum_amount in orders]


async def fetch_top_users():
    async with AsyncSessionLocal() as session:
        last_month_date = date.today() - timedelta(days=30)
        result = await session.execute(
            select(
                Order.user_id,
                func.count(Order.order_id).label("counter"),  # Count of orders
                func.sum(Order.sum).label("summa")  # Total sum spent
            )
            .where(Order.date >= last_month_date)
            .group_by(Order.user_id)
            .order_by(func.sum(Order.sum).desc())
        )
    data = result.all()
    return data




async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)