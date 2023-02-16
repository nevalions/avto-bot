import os
import sys
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineQuery

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))
from src.loader import dp
from src.tg_bot.keybords.inline import ikb_start_menu


@dp.message_handler(commands='inline')
async def show_inline_menu(message: types.Message):
    await message.answer(f'Please select', reply_markup=ikb_start_menu)
