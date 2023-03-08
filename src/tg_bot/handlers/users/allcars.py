import string
import logging.config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_menu, show_delete_cars_menu, \
    show_all_cars_menu, car_action_menu_cd, show_cars_cancel_menu

from src.async_db.base import DATABASE_URL, Database
from src.async_db.tg_users import TgUserService
from src.async_db.cars import CarService
from src.tg_bot.keybords.inline import ikb_cancel_menu

from src.classes import Car

from src.tg_bot.handlers.users.menu_text_helper import separator
from src.tg_bot.handlers.users.helpers import TextMessages, TextCar

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class UpdateCarForm(StatesGroup):
    car_id = State()
    car_model = State()
    car_model_name = State()
    car_current_mileage = State()
    car_description = State()


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    autolog_info("Show all user cars")
    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)
    car_service = CarService(db)
    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(
            int(call.message.chat.id)
        )
        if is_registered.tg_user_id:
            autolog_info(f"Show all tg_user {call.message.chat.id} cars")
            user_id = is_registered.fk_user
            user_cars = await car_service.get_all_user_cars(user_id)
            if user_cars:
                autolog_info(f"tg_user {call.message.chat.id} have some cars")
                for car in user_cars:
                    text = TextCar(car['model'], car['model_name'],
                                   car['current_mileage'], car['measures'],
                                   car['description'])
                    await call.message.answer(text.car_txt(),
                                              reply_markup=show_all_cars_menu(car['id'])
                                              )
                await call.message.answer(separator,
                                          reply_markup=ikb_menu)
            else:
                autolog_warning(f"tg_user {call.message.chat.id} don't have any car")
                await call.message.answer(TextCar().no_car(),
                                          reply_markup=ikb_menu)
        else:
            await call.message.answer(TextCar().no_car(),
                                      reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='cancel'), state='*')
async def cancel_car_action(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    current_state = await state.get_state()
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    try:
        car_id = int(callback_data['car_id'])
        car = await car_service.get_car_by_id(car_id)

        autolog_warning(f'User canceled car id({car.id}) action')
        if current_state is None:
            return

        await state.finish()

        await query.message.answer(
            TextCar.action_canceled_txt(), reply_markup=ikb_menu
        )
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='edit_car_model'))
async def update_inline_car_model(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    car_id = callback_data['car_id']
    autolog_info(f"Edit car id {car_id} model")
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    try:
        car_id = int(callback_data['car_id'])
        car = await car_service.get_car_by_id(car_id)

        async with state.proxy() as data:
            data['car_id'] = car.id
        await UpdateCarForm.car_model.set()
        await query.message.answer(TextCar(car_model=car.model).update_model_txt(),
                                   reply_markup=show_cars_cancel_menu(car_id))
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.message_handler(state=UpdateCarForm.car_model)
async def enter_car_model(message: Message, state: FSMContext):
    autolog_info("Enter new car model")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model "{message.text}"')
            return await message.reply(f'Invalid car model "{message.text}"\n'
                                       f'Enter a valid model',
                                       reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model"{message.text}"\n'
                                   f'Enter a valid model',
                                   reply_markup=ikb_cancel_menu)
    try:
        async with state.proxy() as data:
            data['car_model'] = message.text
            await car_service.update_car_model(int(data['car_id']), data['car_model'])
            await message.answer(TextCar().item_updated_txt(),
                                 reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='edit_car_model_name'))
async def update_inline_car_model_name(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    autolog_info(f"Edit car id {callback_data['car_id']} model name")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    try:
        async with state.proxy() as data:
            car_id = int(callback_data['car_id'])
            data['car_id'] = car_id

            car = await car_service.get_car_by_id(car_id)

        await UpdateCarForm.car_model_name.set()
        await query.message.answer(TextCar(
            car_model=car.model, car_model_name=car.model_name).update_model_name_txt(),
                                   reply_markup=show_cars_cancel_menu(car.id))
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.message_handler(state=UpdateCarForm.car_model_name)
async def enter_car_model_name(message: Message, state: FSMContext):
    autolog_info("Enter new car model name")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model name"{message.text}"')
            return await message.reply(f'Invalid car model name"{message.text}"\n'
                                       f'Enter a valid model name',
                                       reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model name"{message.text}"\n'
                                   f'Enter a valid model name',
                                   reply_markup=ikb_cancel_menu)
    try:
        async with state.proxy() as data:
            data['car_model_name'] = message.text
            await car_service.update_car_model_name(
                int(data['car_id']), data['car_model_name'])
            await message.answer(TextCar().item_updated_txt(),
                                 reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='edit_car_current_mileage'))
async def update_inline_car_current_milage(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    autolog_info(f"Edit car id {callback_data['car_id']} current mileage")
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    try:
        async with state.proxy() as data:
            car_id = int(callback_data['car_id'])
            data['car_id'] = car_id

        car = await car_service.get_car_by_id(car_id)

        await UpdateCarForm.car_current_mileage.set()
        await query.message.answer(
            TextCar.update_car_current_mileage_txt(),
            reply_markup=show_cars_cancel_menu(car.id)
        )
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.message_handler(state=UpdateCarForm.car_current_mileage)
async def enter_car_current_milage(message: Message, state: FSMContext):
    autolog_info("Enter car current milage")
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    try:
        mil = message.text.replace(" ", "").translate(
            str.maketrans('', '', string.punctuation))
        if Car.is_digit(mil):
            autolog_warning(f'Invalid car mileage "{message.text}"')
            return await message.reply(f'Invalid car mileage "{message.text}".\n'
                                       f'Enter a valid mileage.\nJust numbers.',
                                       reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model name"{message.text}"\n'
                                   f'Enter a valid model name',
                                   reply_markup=ikb_cancel_menu)

    try:
        async with state.proxy() as data:
            data['current_mileage'] = mil
            await car_service.update_car_current_mileage(
                int(data['car_id']), int(data['current_mileage']))
            await message.answer(TextCar().item_updated_txt(),
                                 reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='edit_car_description'))
async def update_inline_car_description(
        query: CallbackQuery, callback_data: dict, state: FSMContext):
    autolog_info(f"Edit car id {callback_data['car_id']} description")
    async with state.proxy() as data:
        data['car_id'] = callback_data['car_id']
    await UpdateCarForm.car_description.set()
    await query.message.answer(TextCar().update_description(),
                               reply_markup=show_cars_cancel_menu(
                                   callback_data['car_id']))


@dp.message_handler(state=UpdateCarForm.car_description)
async def enter_car_description(message: Message, state: FSMContext):
    autolog_info("Enter car description")
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    try:
        async with state.proxy() as data:
            data['car_description'] = message.text
            await car_service.update_car_description(
                int(data['car_id']), data['car_description'])
            await message.answer(TextCar().item_updated_txt(),
                                 reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='delete_car'))
async def delete_inline_car(query: CallbackQuery, callback_data: dict):
    autolog_info("Enter car description")
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    autolog_info("Delete car ask")
    car_id = int(callback_data['car_id'])
    car = await car_service.get_car_by_id(car_id)
    markup = await show_delete_cars_menu(car_id)
    delete_text = f'{car.model} {car.model_name}'
    await query.message.answer(TextMessages(text=delete_text).ask_to_delete_txt(),
                               reply_markup=markup)


@dp.callback_query_handler(car_action_menu_cd.filter(action='cancel_delete_car'))
async def cancel_delete_inline_car(query: CallbackQuery, callback_data: dict):
    autolog_warning('Telegram user canceled deleting a car')
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    car_id = int(callback_data['car_id'])
    car = await car_service.get_car_by_id(car_id)
    delete_text = f'{car.model} {car.model_name}'

    await query.message.delete()
    await query.message.answer(TextMessages(delete_text).undo_delete_txt())


@dp.callback_query_handler(car_action_menu_cd.filter(action='delete_car_ok'))
async def delete_car_ok(query: CallbackQuery, callback_data: dict):
    autolog_info("Delete car ok")
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    car_id = int(callback_data['car_id'])
    car = await car_service.get_car_by_id(car_id)

    await car_service.delete_car(car_id)
    await db.engine.dispose()
    await query.message.answer(TextCar(car.model, car.model_name).car_deleted_txt(),
                               reply_markup=ikb_menu)
