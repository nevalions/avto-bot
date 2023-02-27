import logging.config
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_menu, show_delete_cars_menu, show_all_cars_menu, car_action_menu_cd

from async_db.base import DATABASE_URL, Database
from async_db.tg_users import TgUserService
from async_db.cars import CarService


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    autolog_info(f"Show all user's cars")

    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)
    car_service = CarService(db)

    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(int(call.message.chat.id))
        if is_registered.tg_users_id is not None:
            autolog_info(f"Show all tg_user {call.message.chat.id} cars")
            user_id = is_registered.fk_users
            user_cars = await car_service.get_all_user_cars(user_id)
            if user_cars:
                autolog_info(f"tg_user {call.message.chat.id} have some cars")
                for car in user_cars:
                    await call.message.answer(
                        f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                        reply_markup=show_all_cars_menu(int(car['id']))
                    )
                await call.message.answer('Please select from menu', reply_markup=ikb_menu)
            else:
                autolog_warning(f"tg_user {call.message.chat.id} don't have any car")
                await call.message.answer("You don't have any car", reply_markup=ikb_menu)
        else:
            await call.message.answer("You don't have any car", reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='cancel'))
async def cancel_car_action(query: CallbackQuery, callback_data: dict):
    await query.message.answer(
        f'Cancelled.', reply_markup=ReplyKeyboardRemove()
    )


@dp.callback_query_handler(car_action_menu_cd.filter(action='delete'))
async def delete_inline_car(query: CallbackQuery, callback_data: dict):
    autolog_info(f"Delete car")
    print(callback_data['car_id'])
    markup = await show_delete_cars_menu(callback_data['car_id'])
    await query.message.answer(f'Are you sure you want to delete {callback_data["car_id"]}', reply_markup=markup)
