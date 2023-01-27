from aiogram import types
from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu, ikb_menu

from db_tg_users import AutoBotTgUsersDB

db_tg_users = AutoBotTgUsersDB()


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    print(
        message.from_user.id,
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    db_tg_users.add_tg_user_start(
        message.chat.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )

    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', message.chat.id)
        if is_registered[0]['fk_tg_users_users'] is not None:
            await message.answer(f'Welcome back {message.from_user.first_name}!', reply_markup=ikb_menu)
        else:
            await message.answer(f'Hi, {message.from_user.first_name}! Please register.\n' 
                                 'We need some info, to add a garage for you.', reply_markup=ikb_start_menu)
    except Exception as ex:
        print(ex)
