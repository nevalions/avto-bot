from aiogram import Bot, types, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import src.tg_bot.config_tg as config

storage = MemoryStorage()

bot = Bot(token=config.tg_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
