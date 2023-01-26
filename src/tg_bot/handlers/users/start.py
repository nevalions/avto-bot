from aiogram import types
from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu

from db_tg_users import AutoBotTgUsersDB

db_tg_users = AutoBotTgUsersDB()


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    print(message.from_user.id, message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    db_tg_users.add_tg_user_start(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    await message.answer('Please select', reply_markup=ikb_start_menu)
