# Настройка бота - лоадер || токен, секретные ключи, тонкие настройки:
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.webhook import get_new_configured_app
from dotenv import dotenv_values
from pyrogram import Client, enums
from pyrogram.raw.functions.contacts import ResolveUsername
import asyncio
config = dotenv_values(".env")

pyrogram_client = Client(
    "bot",
    api_id=12248750,
    api_hash="988fbe4f5382e515147675e2964703bd",
    bot_token=config["BOT_TOKEN"]
)

bot = Bot(config["BOT_TOKEN"], parse_mode='HTML') # BOT_TOKEN можно || нужно указать в .env

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)