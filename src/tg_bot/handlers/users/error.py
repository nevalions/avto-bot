import os
import sys

from aiogram import types

# sys.path.append(os.path.join(os.getcwd(), '..'))
# sys.path.append(os.path.join(os.getcwd(), '..'))
from src.loader import dp


@dp.message_handler()
async def command_error(message: types.Message):
    await message.answer(f"I don't have command: {message.text}")
