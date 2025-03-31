import asyncio
from create_bot import bot, dp
from handlers import start, calculations, notifications
from apscheduler.triggers.interval import IntervalTrigger
from utils import send_notifications


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from pytz import timezone

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


async def main():
    scheduler.add_job(send_notifications.notify_daily, "cron", hour=12)
    scheduler.add_job(send_notifications.notify_classification, "cron", day=24, hour=18)
    scheduler.start()
    dp.include_routers(start.start_router, calculations.capture_router, notifications.notify_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())