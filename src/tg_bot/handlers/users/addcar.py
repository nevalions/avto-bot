import string
from datetime import datetime

import logging.config
from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

# sys.path.append(os.path.join(os.getcwd(), '..'))
# sys.path.append(os.path.join(os.getcwd(), '..'))
from tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_cancel_menu, ikb_no_description_menu, ikb_km_m_menu, ikb_menu

from src.classes import Car
from src.db import AutoBotTgUsersDB, AutoBotMainDB, AutoBotAutoDB, AutoBotUserDB

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db_user = AutoBotUserDB()
db_auto = AutoBotAutoDB()
db_main = AutoBotMainDB()
db_tg_users = AutoBotTgUsersDB()

now = datetime.now()


class AddCarForm(StatesGroup):
    enter_model = State()
    enter_model_name = State()
    enter_mileage = State()
    enter_measures = State()
    enter_description = State()


@dp.callback_query_handler(text='addcar')
async def add_car_command(call: CallbackQuery, state: FSMContext):
    autolog_info(f"Telegram start adding a car")
    autolog_info(f"{call.message.from_user.id}, {call.message.chat.id}, {call.message.from_user.username}, "
                 f"{call.message.from_user.first_name}, {call.message.from_user.last_name}")
    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', call.message.chat.id)
        if is_registered[0]['fk_tg_users_users'] is not None:
            user_id = is_registered[0]['fk_tg_users_users']
            async with state.proxy() as data:
                data['user_id'] = user_id
        await AddCarForm.enter_model.set()
        await call.message.answer(
            f"Please, enter car model (Lada, Ford, Chevrolet, etc)", reply_markup=ikb_cancel_menu
        )
    except Exception as ex:
        logging.error(ex)


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_inline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    autolog_warning(f'Telegram user canceled adding a car')
    if current_state is None:
        return

    await state.finish()
    db_main.close()
    await call.message.answer(
        'Cancelled.', reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(state=AddCarForm.enter_model)
async def enter_model(message: types.Message, state: FSMContext):
    autolog_info(f'Telegram user added car model')
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model "{message.text}"')
            return await message.reply(f'Invalid car model "{message.text}"\n'
                                       f'Enter a valid model', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model "{message.text}"\n'
                                   f'Enter a valid model', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model'] = message.text

    await AddCarForm.enter_model_name.set()
    await message.answer(f"Enter model name for {data['model']}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_model_name)
async def enter_model_name(message: types.Message, state: FSMContext):
    autolog_info(f'Telegram user added car model name')
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model name "{message.text}"')
            return await message.reply(f'Invalid car model name "{message.text}"\n'
                                       f'Enter a valid model name', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Enter a valid model name', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model_name'] = message.text

    await AddCarForm.enter_mileage.set()
    await message.answer(f"Enter mileage for {data['model']} {data['model_name']}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_mileage)
async def enter_mileage(message: types.Message, state: FSMContext):
    autolog_info(f'Telegram user added car mileage')
    try:
        mil = message.text.replace(" ", "").translate(str.maketrans('', '', string.punctuation))
        if Car.is_digit(mil):
            autolog_warning(f'Invalid car mileage "{message.text}"')
            return await message.reply(f'Invalid car mileage "{message.text}".\n'
                                       f'Enter a valid mileage.\nJust numbers.', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car mileage "{message.text}".\nEnter a valid mileage.\n'
                                   f'Just numbers.', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['mileage'] = mil
        data['current_mileage'] = mil

    await AddCarForm.enter_measures.set()
    await message.answer(f"Enter measures for mileage count (km/miles)", reply_markup=ikb_km_m_menu)


@dp.callback_query_handler(state=AddCarForm.enter_measures, text=['km'])
async def measures_km(call: CallbackQuery, state: FSMContext):
    autolog_info(f'Telegram user added car measures')
    async with state.proxy() as data:
        data['measures'] = 'km'
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        f"Enter description for {data['model']} {data['model_name']}",
        reply_markup=ikb_no_description_menu
    )


@dp.callback_query_handler(state=AddCarForm.enter_measures, text=['miles'])
async def measures_km(call: CallbackQuery, state: FSMContext):
    autolog_info(f'Telegram user added car measures')
    async with state.proxy() as data:
        data['measures'] = 'miles'
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        f"Enter description for {data['model']} {data['model_name']}",
        reply_markup=ikb_no_description_menu
    )


@dp.message_handler(state=AddCarForm.enter_description)
async def enter_description(message: types.Message, state: FSMContext):
    autolog_info(f'Telegram user added car with description')
    async with state.proxy() as data:
        data['description'] = message.text
    try:
        car_id = db_auto.add_car(*vars(Car(
            data['model'],
            data['model_name'],
            data['mileage'],
            data['measures'],
            data['date_added'],
            data['description'],
            data['current_mileage']
        )).values())

        db_main.add_car_to_user_in_db(data['user_id'], car_id)
        autolog_info(f"Car {data['model']}, {data['model_name']}, {data['mileage']} added at {data['date_added']}")
    except Exception as ex:
        logging.error(ex)

    await message.answer(f"{data['model']} {data['model_name']} added at {data['date_added']}",
                         reply_markup=ikb_menu)
    await state.finish()


@dp.callback_query_handler(state=AddCarForm.enter_description, text='no_description')
async def no_description(call: CallbackQuery, state: FSMContext):
    autolog_info(f'Telegram user added car no description ')
    async with state.proxy() as data:
        data['description'] = ''
    try:
        car_id = db_auto.add_car(*vars(Car(
            data['model'],
            data['model_name'],
            data['mileage'],
            data['measures'],
            data['date_added'],
            data['description'],
            data['current_mileage'],
        )).values())

        db_main.add_car_to_user_in_db(data['user_id'], car_id)
        autolog_info(f"Car {data['model']}, {data['model_name']}, {data['mileage']} added at {data['date_added']}")
        await state.finish()
    except Exception as ex:
        logging.error(ex)

    await call.message.answer(f"{data['model']} {data['model_name']} added at {data['date_added']}",
                              reply_markup=ikb_menu)
    await state.finish()
