from aiogram import types

import logging.config
from log_dir.log_conf import LOGGING_CONFIG
from log_dir.func_auto_log import autolog_debug, autolog_info

from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu, ikb_menu

from db_tg_users import AutoBotTgUsersDB

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db_tg_users = AutoBotTgUsersDB()


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    autolog_debug(f'Telegram user started a chat')
    autolog_debug(f"{message.from_user.id}, {message.chat.id}, {message.from_user.username}, "
                  f"{message.from_user.first_name}, {message.from_user.last_name}")

    try:
        autolog_debug(f'new user added DB tg_user after start if not exist in DB')
        db_tg_users.add_tg_user_start(
            message.chat.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
    except Exception as ex:
        logging.error(ex)

    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', message.chat.id)
        if is_registered[0]['fk_tg_users_users'] is not None:
            autolog_info(f'Telegram user {message.chat.id} already registered')
            await message.answer(f'Welcome back {message.from_user.first_name}!', reply_markup=ikb_menu)
        else:
            autolog_info(f'Telegram user {message.chat.id} not registered')
            await message.answer(f'Hi, {message.from_user.first_name}! Please register.\n' 
                                 'We need some info, to add a garage for you.', reply_markup=ikb_start_menu)
    except Exception as ex:
        logging.error(ex)
