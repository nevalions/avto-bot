import logging.config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.async_db.base import DATABASE_URL, Database
from src.async_db.cars import CarService
from src.async_db.maintenances import MaintenanceService
from src.logs.func_auto_log import autolog_info, autolog_warning
from src.logs.log_conf_main import LOGGING_CONFIG
from src.tg_bot.keybords.inline import add_new_maintenance, car_action_menu_cd, \
    ikb_menu, show_all_car_maintenance_menu, show_delete_maintenance_menu, \
    maintenance_action_menu_cd, show_all_maintenance_one_btn, \
    show_maintenance_cancel_menu

from src.tg_bot.handlers.users.helpers import TextMaintenance, TextMessages
from src.tg_bot.handlers.users.menu_text_helper import MenuText

from src.tg_bot.loader import dp

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class UpdateMaintenanceForm(StatesGroup):
    maintenance_title = State()
    maintenance_date = State()
    maintenance_mileage = State()
    maintenance_description = State()
    maintenance_fk_car = State()


@dp.callback_query_handler(car_action_menu_cd.filter(action='show_car_maintenances'))
async def show_cars_maintenances(query: CallbackQuery, callback_data: dict):
    autolog_info("Show all car's maintenances")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    maintenance_service = MaintenanceService(db)
    car = await car_service.get_car_by_id(int(callback_data['car_id']))
    all_maints = await maintenance_service.get_all_car_maintenances(car.id)

    try:
        if all_maints:
            for maint in all_maints:
                text = TextMaintenance(car.model, car.model_name, maint["title"],
                                       maint["date"], maint["maintenance_mileage"],
                                       maint["description"])
                await query.message.answer(text.maintenance(),
                                           reply_markup=show_all_car_maintenance_menu(
                                               maintenance_id=maint["id"],
                                               car_id=car.id))

            await query.message.answer(MenuText.menu_separator(),
                                       reply_markup=add_new_maintenance(
                                           maintenance_id=0, car_id=car.id))

            await query.message.answer(MenuText.menu_separator(),
                                       reply_markup=ikb_menu)
        else:
            autolog_warning(
                f"Car: {car.model} {car.model_name}\n don't have any maintenances")
            await query.message.answer(
                f"Car: {car.model} {car.model_name}\n"
                f"Does not have any maintenances",
                reply_markup=add_new_maintenance(maintenance_id=0, car_id=car.id))

            await query.message.answer(MenuText.menu_separator(), reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='cancel'), state='*')
async def cancel_maintenance_action(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    current_state = await state.get_state()
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)

    m_id = int(callback_data['maintenance_id'])
    maint = await maintenance_service.get_car_maintenance_by_id(m_id)

    autolog_warning(f'User canceled maintenance id({maint.id}) action')
    if current_state is None:
        return

    await state.finish()
    await db.engine.dispose()
    await query.message.answer(
        'Action cancelled.', reply_markup=show_all_maintenance_one_btn(
            car_id=maint.fk_car)
    )


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='edit_maintenance_title'))
async def update_inline_maintenance_title(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    m_id = int(callback_data['maintenance_id'])
    c_id = int(callback_data['car_id'])

    autolog_info(f"Edit maintenance id({m_id}) title")
    async with state.proxy() as data:
        data['m_id'] = m_id
    await UpdateMaintenanceForm.maintenance_title.set()
    await query.message.answer('Enter new maintenance title',
                               reply_markup=show_maintenance_cancel_menu(
                                   maintenance_id=m_id, car_id=c_id))


@dp.message_handler(state=UpdateMaintenanceForm.maintenance_title)
async def enter_maint_title(message: Message, state: FSMContext):
    autolog_info("Enter new maintenance title")
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)

    try:
        async with state.proxy() as data:
            m_id = int(data['m_id'])
            maint = await maintenance_service.get_car_maintenance_by_id(m_id)
            await maintenance_service.update_maintenance_title(
                maint.id, message.text)
            await message.answer('✅ Maintenance title updated',
                                 reply_markup=show_all_maintenance_one_btn(
                                     car_id=maint.fk_car))
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='delete_maintenance'))
async def delete_inline_maintenance(query: CallbackQuery, callback_data: dict):
    m_id = int(callback_data['maintenance_id'])
    autolog_info(f"Delete maintenance id({m_id}) ask")

    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)

    maint = await maintenance_service.get_car_maintenance_by_id(m_id)
    markup = await show_delete_maintenance_menu(
        maintenance_id=maint.id, car_id=maint.fk_car)

    text = TextMessages(text=maint.title)
    await query.message.answer(
        text.ask_to_delete(),
        reply_markup=markup)

    await db.engine.dispose()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='cancel_delete_maintenance'))
async def cancel_delete_inline_maintenance(query: CallbackQuery, callback_data: dict):
    m_id = int(callback_data['maintenance_id'])
    autolog_warning(f'Telegram user canceled deleting a maintenance id'
                    f'({m_id})')

    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)
    try:
        maint = await maintenance_service.get_car_maintenance_by_id(m_id)

        await query.message.delete()
        await query.message.answer(f'Maintenance {maint.title} deleting cancelled.',
                                   reply_markup=show_all_maintenance_one_btn(
                                       car_id=maint.fk_car))
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(
    action='delete_maintenance_ok'))
async def delete_maintenance_ok(query: CallbackQuery, callback_data: dict):
    m_id = int(callback_data['maintenance_id'])
    autolog_info(f'Delete maintenance id({m_id}) OK')

    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)
    try:
        maint = await maintenance_service.get_car_maintenance_by_id(m_id)
        text = TextMaintenance(maint_title=maint.title)
        await query.message.delete()
        await maintenance_service.delete_maintenance(maint.id)
        await query.message.answer(text.maintenance_deleted(),
                                   reply_markup=show_all_maintenance_one_btn(
                                       car_id=maint.fk_car))
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()
