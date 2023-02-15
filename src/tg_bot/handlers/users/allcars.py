import logging.config
from aiogram.types import CallbackQuery

from loader import dp

from tg_bot.keybords.inline import ikb_car_menu, ikb_menu

from db.db_main_helper import AutoBotMainDB
from db.db_tg_users import AutoBotTgUsersDB

from src.log_dir.log_conf import LOGGING_CONFIG
from src.log_dir.func_auto_log import autolog_warning, autolog_info

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db_main = AutoBotMainDB()
db_tg_users = AutoBotTgUsersDB()


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    autolog_info(f"Show all user's cars")
    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', call.message.chat.id)
        if is_registered[0]['fk_tg_users_users'] is not None:
            autolog_info(f"Show all tg_user {call.message.chat.id} cars")
            user_id = is_registered[0]['fk_tg_users_users']
            user_cars = db_main.show_all_users_cars(user_id)
            if user_cars:
                autolog_info(f"tg_user {call.message.chat.id} have some cars")
                for car in user_cars:
                    await call.message.answer(
                        f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                        reply_markup=ikb_car_menu
                    )
                await call.message.answer('Please select from menu', reply_markup=ikb_menu)
            else:
                autolog_warning(f"tg_user {call.message.chat.id} don't have any car")
                await call.message.answer("You don't have any car", reply_markup=ikb_menu)
        else:
            await call.message.answer("You don't have any car", reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)

