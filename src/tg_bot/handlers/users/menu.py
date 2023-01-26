from aiogram import types
from aiogram.dispatcher.filters import Command

from src.tg_bot.loader import dp
from src.tg_bot.keybords.default import kb_menu


@dp.message_handler(Command('menu'))
async def menu(message: types.Message):
    await message.answer('Select from menu', reply_markup=kb_menu)
