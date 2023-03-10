import string
from datetime import datetime

import logging.config
from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_cancel_menu, ikb_no_description_menu, \
    ikb_km_m_menu, ikb_menu, ikb_start_menu

from src.classes import Car

from src.tg_bot.handlers.users.helpers import TextCar, TextMessages

from src.async_db.base import DATABASE_URL, Database
from src.async_db.tg_users import TgUserService
from src.async_db.cars import CarService

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

now = datetime.now()


class AddCarForm(StatesGroup):
    enter_model = State()
    enter_model_name = State()
    enter_mileage = State()
    enter_measures = State()
    enter_description = State()


@dp.callback_query_handler(text='addcar')
async def add_car_command(call: CallbackQuery, state: FSMContext):
    autolog_info("Telegram start adding a car")
    autolog_info(f"{call.message.from_user.id}, "
                 f"{call.message.chat.id}, "
                 f"{call.message.from_user.username}, "
                 f"{call.message.from_user.first_name}, "
                 f"{call.message.from_user.last_name}")

    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)

    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(
            int(call.message.chat.id))
        if is_registered.tg_user_id:
            user_id = is_registered.fk_user
            async with state.proxy() as data:
                data['user_id'] = user_id
            await AddCarForm.enter_model.set()
            await call.message.answer(
                TextCar.add_car_model_txt(),
                reply_markup=ikb_cancel_menu
            )
        else:
            autolog_warning(f'Telegram user {call.message.chat.id} not registered')
            await call.message.answer(TextMessages.register_txt(),
                                      reply_markup=ikb_start_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_inline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    autolog_warning('Telegram user canceled adding a car')
    if current_state is None:
        return

    await state.finish()
    await call.message.answer(
        TextMessages.action_canceled_txt(),
        reply_markup=ReplyKeyboardRemove()
    )


@dp.message_handler(state=AddCarForm.enter_model)
async def enter_model(message: Message, state: FSMContext):
    autolog_info('Telegram user added car model')
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model "{message.text}"')
            return await message.reply(f'Invalid car model "{message.text}"\n'
                                       f'Enter a valid model',
                                       reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model "{message.text}"\n'
                                   f'Enter a valid model',
                                   reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model'] = message.text

    await AddCarForm.enter_model_name.set()
    await message.answer(TextCar(car_model_name=data['model']).add_car_model_name_txt(),
                         reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_model_name)
async def enter_model_name(message: Message, state: FSMContext):
    autolog_info('Telegram user added car model name')
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model name "{message.text}"')
            return await message.reply(f'Invalid car model name "{message.text}"\n'
                                       f'Enter a valid model name',
                                       reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply('Enter a valid model name',
                                   reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model_name'] = message.text

    await AddCarForm.enter_mileage.set()
    await message.answer(
        TextCar(
            car_model=data['model'],
            car_model_name=data['model_name']).add_car_mileage_txt(),
        reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_mileage)
async def enter_mileage(message: Message, state: FSMContext):
    autolog_info('Telegram user added car mileage')
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
        return await message.reply(f'Invalid car mileage "{message.text}"'
                                   f'\nEnter a valid mileage.\n'
                                   f'Just numbers.', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['mileage'] = mil
        data['current_mileage'] = mil

    await AddCarForm.enter_measures.set()
    await message.answer(
        TextCar(
            car_model=data['model'],
            car_model_name=data['model_name'],
            current_mileage=data['mileage']).add_car_measure_txt(),
        reply_markup=ikb_km_m_menu)


@dp.callback_query_handler(state=AddCarForm.enter_measures, text=['km'])
async def measures_km(call: CallbackQuery, state: FSMContext):
    autolog_info('Telegram user added car measures')
    async with state.proxy() as data:
        data['measures'] = 'km'
        data['date_added'] = f'{datetime.utcnow()}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        TextCar(
            car_model=data['model'],
            car_model_name=data['model_name'],
            current_mileage=data['mileage'],
            measures=data['measures']).add_car_description_txt(),
        reply_markup=ikb_no_description_menu
    )


@dp.callback_query_handler(state=AddCarForm.enter_measures, text=['miles'])
async def measures_miles(call: CallbackQuery, state: FSMContext):
    autolog_info('Telegram user added car measures')
    async with state.proxy() as data:
        data['measures'] = 'miles'
        data['date_added'] = f'{datetime.utcnow()}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        TextCar(
            car_model=data['model'],
            car_model_name=data['model_name'],
            current_mileage=data['mileage'],
            measures=data['measures']).add_car_description_txt(),
        reply_markup=ikb_no_description_menu
    )


@dp.message_handler(state=AddCarForm.enter_description)
async def enter_description(message: Message, state: FSMContext):
    autolog_info('Telegram user added car with description')
    db = Database(DATABASE_URL)
    car_service = CarService(db)

    async with state.proxy() as data:
        data['description'] = message.text
    try:
        car = await car_service.add_car(
            data['model'],
            data['model_name'],
            int(data['mileage']),
            data['measures'],
            data['description'],
            fk_user=data['user_id']
        )

        autolog_info(
            f"Car {car.model}, {car.model_name}, {car.mileage} "
            f"added at {car.date_added.isoformat()}\n"
            f"Description: {car.description}")
        text_car = TextCar(
            car_model=car.model,
            car_model_name=car.model_name,
            current_mileage=car.mileage,
            measures=car.measures,
            description=car.description
        )
        await message.answer(
            f'{text_car.car_txt()}\n{text_car.added_txt()}',
            reply_markup=ikb_menu)

    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()


@dp.callback_query_handler(state=AddCarForm.enter_description, text='no_description')
async def no_description(call: CallbackQuery, state: FSMContext):
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    autolog_info('Telegram user added car no description ')
    async with state.proxy() as data:
        data['description'] = ''
    try:
        car = await car_service.add_car(
            data['model'],
            data['model_name'],
            int(data['mileage']),
            data['measures'],
            data['description'],
            fk_user=data['user_id']
        )

        autolog_info(
            f"Car {car.model}, {car.model_name}, {car.mileage} "
            f"added at {car.date_added.isoformat()}"
            f"Description: {car.description}")
        text_car = TextCar(
            car_model=car.model,
            car_model_name=car.model_name,
            current_mileage=car.mileage,
            measures=car.measures,
            description=car.description
        )
        await call.message.answer(
            f'{text_car.car_txt()}\n{text_car.added_txt()}',
            reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await state.finish()
        await db.engine.dispose()
