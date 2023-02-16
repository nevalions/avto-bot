from aiogram import types
import os
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))

from src.loader import dp

from src.tg_bot.keybords.inline import ikb_menu


@dp.message_handler(commands='menu')
async def inline_menu(message: types.Message):
    await message.answer('Menu', reply_markup=ikb_menu)
