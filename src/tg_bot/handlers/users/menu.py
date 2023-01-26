from aiogram import types
from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_menu


@dp.message_handler(commands='menu')
async def inline_menu(message: types.Message):
    await message.answer('Menu', reply_markup=ikb_menu)
