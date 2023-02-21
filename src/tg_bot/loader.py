from aiogram import Bot, types, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.tg_bot.config_tg import tg_token

storage = MemoryStorage()

bot = Bot(token=tg_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
