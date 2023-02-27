from aiogram import types

import logging.config

from src.async_db.base import DATABASE_URL, Database
from src.async_db.tg_users import TgUserService

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_start_menu, ikb_menu

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@dp.message_handler(commands='start')
async def inline_start_menu(message: types.Message):
    autolog_info(f'Telegram user started a chat')
    autolog_info(f"{message.from_user.id}, {message.chat.id}, {message.from_user.username}, "
                 f"{message.from_user.first_name}, {message.from_user.last_name}")

    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)

    try:
        autolog_info(f'new user added to DB tg_user after start if not exist in DB')
        await tg_user_service.add_tg_user(
            int(message.chat.id),
            message.from_user.username,
            message.from_user.first_name,
            message.from_user.last_name
        )
    except Exception as ex:
        logging.error(ex)

    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(int(message.chat.id))
        if is_registered.tg_users_id is not None:
            autolog_warning(f'Telegram user {message.chat.id} already registered')
            await message.answer(f'Welcome back {message.from_user.first_name}!', reply_markup=ikb_menu)
        else:
            autolog_warning(f'Telegram user {message.chat.id} not registered')
            await message.answer(f'Hi, {message.from_user.first_name}! Please register.\n'
                                 f'We need some info, to add a garage for you.', reply_markup=ikb_start_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()
