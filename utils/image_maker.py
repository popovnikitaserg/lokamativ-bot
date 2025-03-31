import asyncio
from great_tables import GT
import polars as pl

from create_bot import managers_name

from db_handlers import db_func

async def best_managers():
    res = await db_func.fetch_top_users()
    format_res = [(rank + 1, managers_name[id], counter, summa) for rank, (id, counter, summa) in enumerate(res)]
    df = pl.DataFrame(format_res, schema=["Rank", "Менеджер", "Количество", "Сумма"], orient="row")

    table = (
        GT(df, rowname_col="Rank")
        .tab_header("Топ менеджеров по заявкам")
    )
    GT.save(table, "../statistics.png", scale=1.5)