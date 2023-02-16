from aiogram import types

import logging.config
from .logs.log_conf_main import LOGGING_CONFIG
from .logs.func_auto_log import autolog_warning, autolog_info

import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append(os.path.join(os.getcwd(), '..'))

print(sys.path)

from src.loader import dp

from src.tg_bot.keybords.inline import ikb_start_menu, ikb_menu

from src.db import AutoBotTgUsersDB, AutoBotMainDB

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db_tg_users = AutoBotTgUsersDB()
db_main = AutoBotMainDB()


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    autolog_info(f'Telegram user started a chat')
    autolog_info(f"{message.from_user.id}, {message.chat.id}, {message.from_user.username}, "
                 f"{message.from_user.first_name}, {message.from_user.last_name}")

    try:
        autolog_info(f'new user added to DB tg_user after start if not exist in DB')
        db_tg_users.add_tg_user_start(
            message.chat.id,
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
        db_main.close()
    except Exception as ex:
        logging.error(ex)

    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', message.chat.id)
        db_main.close()
        if is_registered[0]['fk_tg_users_users'] is not None:
            autolog_warning(f'Telegram user {message.chat.id} already registered')
            await message.answer(f'Welcome back {message.from_user.first_name}!', reply_markup=ikb_menu)
        else:
            autolog_warning(f'Telegram user {message.chat.id} not registered')
            await message.answer(f'Hi, {message.from_user.first_name}! Please register.\n'
                                 f'We need some info, to add a garage for you.', reply_markup=ikb_start_menu)
    except Exception as ex:
        logging.error(ex)
