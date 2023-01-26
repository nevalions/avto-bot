from aiogram import types
from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu


# @dp.message_handler(commands=['start', 'help'])
# async def command_start(message: types.Message):
#     # say hello to user and get tg.id
#     print(
#         message.from_user.id,
#         message.from_user.username,
#         message.from_user.first_name,
#         message.from_user.last_name)
#
#     await message.answer(
#         f'Hi, {message.from_user.first_name}!\n'
#         f'If you want to use AutoBot /register first\n'
#         f'If you are already registered you can /addcar\n'
#         f'Show all cars /allcars'
#     )


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    await message.answer('Please select', reply_markup=ikb_start_menu)
