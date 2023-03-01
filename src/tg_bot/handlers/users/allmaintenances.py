import string
import logging.config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_menu, show_all_car_maintenance_menu, show_delete_maintenance_menu, \
    show_maintenance_cancel_menu, car_action_menu_cd, maintenance_action_menu_cd, add_new_maintenance

from src.async_db.base import DATABASE_URL, Database
from src.async_db.cars import CarService
from src.async_db.maintenances import MaintenanceService

from src.tg_bot.handlers.users import helpers

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class UpdateCarForm(StatesGroup):
    maintenance_id = State()
    maintenance_title = State()
    maintenance_date = State()
    maintenance_current_mileage = State()
    maintenance_description = State()
    maintenance_fk_car = State()


@dp.callback_query_handler(car_action_menu_cd.filter(action='show_car_maintenances'))
async def show_cars_maintenances(query: CallbackQuery, callback_data: dict):
    autolog_info(f"Show all car's maintenances")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    maintenance_service = MaintenanceService(db)
    # try:
    car_id = int(callback_data['car_id'])
    all_maints = await maintenance_service.get_all_car_maintenances(car_id)

    for maint in all_maints:
        car = await car_service.get_car_by_id(car_id)
        await query.message.answer(
            f'Car: {car.model} {car.model_name}\n'
            f'Maintenance: {maint["title"]}\n'
            f'Date: {maint["date"]}\n'
            f'Current mileage: {maint["current_mileage"]}\n',

            reply_markup=show_all_car_maintenance_menu(maintenance_id=0, car_id=car_id)
        )

    await query.message.answer('Add new maintenance',
                               reply_markup=add_new_maintenance(maintenance_id=0, car_id=car_id))

    await query.message.answer(f'Main menu', reply_markup=ikb_menu)

        #
        # is_registered = await tg_user_service.get_tg_user_by_chat_id(int(query.message.chat.id))
        # if is_registered.tg_user_id:
        #     autolog_info(f"Show all tg_user {query.message.chat.id} cars")
        #     user_id = is_registered.fk_user
        #     user_cars = await car_service.get_all_user_cars(user_id)
        #     if user_cars:
        #         autolog_info(f"tg_user {query.message.chat.id} have some cars")
        #         for car in user_cars:
        #             await query.message.answer(
        #                 f"ID({car['id']}) {car['model']} {car['model_name']} with current {car['current_mileage']} "
        #                 f"{car['measures']}\n"
        #                 f"Info: {car['description']}",
        #                 reply_markup=show_all_car_maintenance_menu(car['id'])
        #             )
        #     else:
        #         autolog_warning(f"tg_user {query.message.chat.id} don't have any car")
        #         await query.message.answer("Car don't have any maintenances", reply_markup=ikb_menu)
        # else:
        #     await query.message.answer("Car don't have any maintenances", reply_markup=ikb_menu)
    # except Exception as ex:
    #     logging.error(ex)
    # finally:
    #     await db.engine.dispose()
