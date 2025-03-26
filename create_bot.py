import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

destinations = {
    1: {"dest" : "Склад Санкт-Петербург - Склад Калининград"},
    2: {"dest" : "Склад Калининград - Склад Санкт-Петербург"}
}

managers = [
    ("Анна", "+79673535916"),
    ("Анастасия",  "+79632994969"),
    ("Юлия", "+79062327792"),
    ("Софья", "+79097792733"),
    ("Александра", "+79622581157"),
    ("Ольга", "+79097791965"),
    ("Алина", "+79052446248"),
    ("Анна", "+79034054146"),
    ("Алевтина", "+79622625783")
]