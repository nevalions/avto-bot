import logging.config

from aiogram.types import CallbackQuery, Message

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_menu, show_all_car_maintenance_menu, show_delete_maintenance_menu, \
    show_maintenance_cancel_menu, car_action_menu_cd, maintenance_action_menu_cd, add_new_maintenance

from src.async_db.base import DATABASE_URL, Database
from src.async_db.cars import CarService
from src.async_db.maintenances import MaintenanceService

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@dp.callback_query_handler(car_action_menu_cd.filter(action='show_car_maintenances'))
async def show_cars_maintenances(query: CallbackQuery, callback_data: dict):
    autolog_info(f"Show all car's maintenances")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    maintenance_service = MaintenanceService(db)
    car_id = int(callback_data['car_id'])
    car = await car_service.get_car_by_id(car_id)
    all_maints = await maintenance_service.get_all_car_maintenances(car_id)
    try:
        if all_maints:
            for maint in all_maints:
                await query.message.answer(
                    f'Car: {car.model} {car.model_name}\n'
                    f'Maintenance: {maint["title"]}\n'
                    f'Date: {maint["date"]}\n'
                    f'Maintenance mileage: {maint["maintenance_mileage"]}\n',

                    reply_markup=show_all_car_maintenance_menu(maintenance_id=0, car_id=car_id)
                )

            await query.message.answer('Add new maintenance',
                                       reply_markup=add_new_maintenance(maintenance_id=0, car_id=car_id))

            await query.message.answer(f'Main menu', reply_markup=ikb_menu)
        else:
            autolog_warning(f"Car: {car.model} {car.model_name}\n don't have any maintenances")
            await query.message.answer(
                f"Car: {car.model} {car.model_name}\n"
                f"Does not have any maintenances",
                reply_markup=add_new_maintenance(maintenance_id=0, car_id=car_id))

            await query.message.answer(f'Main menu', reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()
