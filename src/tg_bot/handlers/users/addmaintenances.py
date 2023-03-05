import logging.config
import string

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_calendar import SimpleCalendar, simple_cal_callback

from src.async_db.base import DATABASE_URL, Database
from src.async_db.cars import CarService
from src.async_db.maintenances import MaintenanceService
from src.classes.cars import Car
from src.logs.func_auto_log import autolog_info, autolog_warning
from src.logs.log_conf_main import LOGGING_CONFIG
from src.tg_bot.keybords.inline import (ikb_cancel_menu,
                                        ikb_no_description_menu,
                                        maintenance_action_menu_cd,
                                        show_all_car_maintenance_menu)
from src.tg_bot.loader import dp

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class AddMaintenanceForm(StatesGroup):
    maintenance_title = State()
    maintenance_date = State()
    maintenance_mileage = State()
    maintenance_description = State()
    maintenance_fk_car = State()


@dp.callback_query_handler(maintenance_action_menu_cd.filter(action='add_car_maintenances'))
async def add_car_maintenance_id(
        query: CallbackQuery, callback_data: dict, state: FSMContext
):
    autolog_info("Add car maintenances")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    car_id = int(callback_data['car_id'])
    car = await car_service.get_car_by_id(car_id)
    try:
        if car:
            async with state.proxy() as data:
                data['maintenance_fk_car'] = car_id
            await AddMaintenanceForm.maintenance_title.set()
            await query.message.answer(
                f"Please, enter maintenance"
                f"title for car {car.model} {car.model_name}",
                reply_markup=ikb_cancel_menu
            )

        else:
            print('LOL kek no Car')
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.message_handler(state=AddMaintenanceForm.maintenance_title)
async def add_car_maintenance_title(
        message: Message, state: FSMContext
):

    autolog_info('Add car maintenances title')

    async with state.proxy() as data:
        data['maintenance_title'] = message.text

    await AddMaintenanceForm.maintenance_date.set()
    await message.answer("Please select a date:",
                         reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(
    simple_cal_callback.filter(),
    state=AddMaintenanceForm.maintenance_date
)
async def add_car_maintenance_date(
    query: CallbackQuery,
    callback_data: dict,
    state: FSMContext
):
    autolog_info('Add car maintenances date')
    selected, date = await SimpleCalendar().process_selection(query, callback_data)
    print(selected, date)
    if not selected:
        return None
    else:
        async with state.proxy() as data:
            data['maintenance_date'] = date
        # await query.message.answer(
        #     f'You selected {date.strftime("%d/%m/%Y")}',
        # )

    await AddMaintenanceForm.maintenance_mileage.set()
    await query.message.answer("Enter maintenances mileage",
                               reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddMaintenanceForm.maintenance_mileage)
async def add_car_maintenance_mileage(
        message: Message, state: FSMContext
):
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    autolog_info('Add car maintenances mileage')
    try:
        mil = message.text.replace(" ", "").translate(
            str.maketrans('', '', string.punctuation))
        if Car.is_digit(mil):
            autolog_warning(f'Invalid car mileage "{message.text}"')
            return await message.reply(f'Invalid car mileage "{message.text}".\n'
                                       f'Enter a valid mileage.\nJust numbers.',
                                       reply_markup=ikb_cancel_menu)
        else:
            async with state.proxy() as data:
                data['maintenance_mileage'] = mil

            await car_service.update_car_current_mileage(
                int(data['maintenance_fk_car']),
                int(data['maintenance_mileage'])
            )
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car mileage "{message.text}".\n'
                                   f'Enter a valid mileage.\n'
                                   f'Just numbers.', reply_markup=ikb_cancel_menu)

    await AddMaintenanceForm.maintenance_description.set()
    await message.answer(
        "Enter maintenances description", reply_markup=ikb_no_description_menu)


@dp.message_handler(state=AddMaintenanceForm.maintenance_description)
async def add_car_maintenance_description(
        message: Message, state: FSMContext
):
    autolog_info('Add car maintenances description')
    db = Database(DATABASE_URL)
    maint_service = MaintenanceService(db)

    async with state.proxy() as data:
        data['maintenance_description'] = message.text

        maint = await maint_service.add_maintenance(
            title=data['maintenance_title'],
            date=data['maintenance_date'],
            maintenance_mileage=int(data['maintenance_mileage']),
            description=data['maintenance_description'],
            fk_car=int(data['maintenance_fk_car'])
        )

    print(maint)

    await show_all_car_maintenance_menu()

    await state.finish()
    await db.engine.dispose()


@dp.callback_query_handler(
    state=AddMaintenanceForm.maintenance_description,
    text='no_description'
)
async def no_description(query: CallbackQuery, state: FSMContext):
    autolog_info('Add car maintenances description')
    db = Database(DATABASE_URL)
    maint_service = MaintenanceService(db)

    async with state.proxy() as data:
        data['maintenance_description'] = ''

        maint = await maint_service.add_maintenance(
            title=data['maintenance_title'],
            date=data['maintenance_date'],
            maintenance_mileage=int(data['maintenance_mileage']),
            description=data['maintenance_description'],
            fk_car=int(data['maintenance_fk_car'])
        )

    print(maint)

    await show_all_car_maintenance_menu()

    await state.finish()
    await db.engine.dispose()
