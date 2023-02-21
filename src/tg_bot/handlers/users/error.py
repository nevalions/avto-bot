from aiogram import types

from src.tg_bot.loader import dp


@dp.message_handler()
async def command_error(message: types.Message):
    await message.answer(f"I don't have command: {message.text}")
