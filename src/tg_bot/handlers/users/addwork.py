import logging.config
import string

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from src.async_db.base import DATABASE_URL, Database
from src.async_db.maintenances import MaintenanceService
from src.async_db.works import WorkService
# from src.async_db.maints_works import MaintWorkService

from src.classes.cars import Car
from src.logs.func_auto_log import autolog_info, autolog_warning
from src.logs.log_conf_main import LOGGING_CONFIG
from src.tg_bot.keybords.inline import ikb_cancel_menu, ikb_no_description_menu, \
    maintenance_action_menu_cd, show_all_maintenance_one_btn, show_cars_cancel_menu, \
    work_action_menu_cd, show_all_works_menu

from src.tg_bot.handlers.users.helpers import TextMaintenance

from src.tg_bot.loader import dp

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class AddWorkForm(StatesGroup):
    work_title = State()
    work_description = State()
    work_is_regular = State()
    work_next_maintenance = State()
    work_fk_maint = State()


@dp.callback_query_handler(work_action_menu_cd.filter(
    action='add_work'))
async def add_work_title(
        query: CallbackQuery, callback_data: dict, state: FSMContext
):
    autolog_info("Add work")
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)
    maint_id = int(callback_data['maintenance_id'])
    maint = await maintenance_service.get_car_maintenance_by_id(maint_id)
    try:
        if maint:
            async with state.proxy() as data:
                data['fk_maintenance'] = maint.id
            # text = TextMaintenance(car_model=car.model, car_model_name=car.model_name)

            await AddWorkForm.work_title.set()
            await query.message.answer('Add title')
        else:
            autolog_info("PROBLEM WORK!")
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.message_handler(state=AddWorkForm.work_title)
async def add_work(message: Message, state: FSMContext):
    autolog_info("Enter work title")
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)
    work_service = WorkService(db)

    try:
        async with state.proxy() as data:
            maint_id = data['fk_maintenance']
            result = await maintenance_service.join_maintenance_and_car(maint_id)
            user_id = result['car']['fk_user']

            work = await work_service.add_work(
                title=message.text,
                is_regular=True,
                next_maintenance_after=int(1111),
                description='',
                is_custom=True,
                fk_user=user_id,
                m_id=maint_id
            )

            print(work.id)

            await message.answer('work added', reply_markup=show_all_works_menu(
                work_id=work.id, maintenance_id=maint_id
            ))

    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


