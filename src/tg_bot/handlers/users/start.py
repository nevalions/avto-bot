from aiogram import types
from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    await message.answer('Please select', reply_markup=ikb_start_menu)
