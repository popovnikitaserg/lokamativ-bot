import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

engine = create_async_engine(config("PG_LINK"), echo=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

admins = [1080904683, 1056335508, 1063597034]
managers_id = [1388763627, 7625713212, 7164032705, 7998140593, 6071533860, 1437113542, 1897908313]
managers_name = {1388763627: "Аля", 7625713212: "Аня", 7164032705: "Ольга", 7998140593:"Настя", 6071533860:"Юлия", 1437113542:"Софья", 1897908313:"Алина"}


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