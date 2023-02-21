from aiogram import Bot, types, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config_tg

storage = MemoryStorage()

bot = Bot(token=config_tg.tg_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
