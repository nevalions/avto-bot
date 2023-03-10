import logging.config
import string

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.async_db.base import DATABASE_URL, Database
from src.async_db.works import WorkService
from src.async_db.maintenances import MaintenanceService
from src.logs.func_auto_log import autolog_info, autolog_warning
from src.logs.log_conf_main import LOGGING_CONFIG

from src.tg_bot.keybords.inline import add_new_maintenance, car_action_menu_cd, \
    ikb_menu, show_all_car_maintenance_menu, show_delete_maintenance_menu, \
    maintenance_action_menu_cd, show_all_maintenance_one_btn, \
    show_maintenance_cancel_menu, ikb_cancel_menu, show_all_works_menu, \
    work_action_menu_cd, add_new_work

from src.tg_bot.handlers.users.helpers import TextMaintenance, TextMessages
from src.tg_bot.handlers.users.menu_text_helper import MenuText

from src.classes import Car

from src.tg_bot.loader import dp

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class UpdateWorkForm(StatesGroup):
    work_title = State()
    work_description = State()
    work_is_regular = State()
    work_next_maintenance_after = State()
    work_fk_car = State()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='maintenance_works'))
async def show_maintenance_works(query: CallbackQuery, callback_data: dict):
    autolog_info("Show all maintenance work")
    db = Database(DATABASE_URL)
    work_service = WorkService(db)
    maintenance_service = MaintenanceService(db)

    maint = await maintenance_service.get_car_maintenance_by_id(
        int(callback_data['maintenance_id']))
    car_maint_join = await maintenance_service.join_maintenance_and_car(maint.id)

    # all_maints_works = await work_service.get_all_user_custom_works(
    #     car_maint_join["car"]["fk_user"])

    await query.message.answer(
        'No works',
        reply_markup=show_all_works_menu(work_id=0, maintenance_id=0))

    await query.message.answer('Add work',
                               reply_markup=add_new_work(
                                   work_id=0, maintenance_id=int(callback_data['maintenance_id']))
                               )

    # try:
    #     if all_maints:
    #         for maint in all_maints:
    #             text = TextMaintenance(car.model, car.model_name, maint["title"],
    #                                    maint["date"], maint["maintenance_mileage"],
    #                                    maint["description"])
    #             await query.message.answer(text.maintenance_txt(),
    #                                        reply_markup=show_all_car_maintenance_menu(
    #                                            maintenance_id=maint["id"],
    #                                            car_id=car.id))
    #
    #         await query.message.answer(MenuText.menu_separator(),
    #                                    reply_markup=add_new_maintenance(
    #                                        maintenance_id=0, car_id=car.id))
    #
    #         await query.message.answer(MenuText.menu_separator(),
    #                                    reply_markup=ikb_menu)
    #     else:
    #         autolog_warning(
    #             f"Car: {car.model} {car.model_name}\n don't have any maintenances")
    #
    #         await query.message.answer(
    #             TextMaintenance(car.model, car.model_name).no_maintenance_txt(),
    #             reply_markup=add_new_maintenance(maintenance_id=0, car_id=car.id))

    # except Exception as ex:
    #     logging.error(ex)
    # finally:
    #     await db.engine.dispose()
