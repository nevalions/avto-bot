import string
from datetime import datetime
from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from src.tg_bot.loader import dp
from tg_bot.keybords.inline import ikb_cancel_menu, ikb_no_description_menu, ikb_km_m_menu, ikb_menu

from users import User
from cars import Car

from db_user_helper import AutoBotUserDB
from db_auto_helper import AutoBotAutoDB
from db_main_helper import AutoBotMainDB

db_user = AutoBotUserDB()
db_auto = AutoBotAutoDB()
db_main = AutoBotMainDB()

now = datetime.now()


class AddCarForm(StatesGroup):
    enter_model = State()
    enter_model_name = State()
    enter_mileage = State()
    enter_measures = State()
    enter_description = State()


@dp.message_handler(commands=['addcar'])
async def addcar_command(message: types.Message):
    await AddCarForm.enter_model.set()
    await message.answer(
        f'Please, enter car model (Lada, Ford, Chevrolet, etc)', reply_markup=ikb_cancel_menu
    )


@dp.callback_query_handler(text='addcar')
async def register_command_inline(call: CallbackQuery):
    await AddCarForm.enter_model.set()
    await call.message.answer(
        f'Please, enter car model (Lada, Ford, Chevrolet, etc)', reply_markup=ikb_cancel_menu
    )


@dp.callback_query_handler(state='*', text='cancel')
async def register_command_inline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await call.message.answer(
        'Cancelled.', reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=AddCarForm.enter_model)
async def enter_model(message: types.Message, state: FSMContext):
    try:
        if Car.not_empty_str(message.text):
            return await message.reply('Enter a valid model', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid model', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model'] = message.text

    await AddCarForm.enter_model_name.set()
    await message.answer(f"Enter model name for {data['model']}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_model_name)
async def enter_model_name(message: types.Message, state: FSMContext):
    try:
        if Car.not_empty_str(message.text):
            return await message.reply('Enter a valid model name', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid model name', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['model_name'] = message.text

    await AddCarForm.enter_mileage.set()
    await message.answer(f"Enter mileage for {data['model']} {data['model_name']}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=AddCarForm.enter_mileage)
async def enter_mileage(message: types.Message, state: FSMContext):
    try:
        mil = message.text.replace(" ", "").translate(str.maketrans('', '', string.punctuation))
        if Car.is_digit(mil):
            return await message.reply('Enter a valid mileage', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid mileage', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['mileage'] = mil

    await AddCarForm.enter_measures.set()
    await message.answer(f"Enter measures for mileage count (km/miles)", reply_markup=ikb_km_m_menu)


@dp.callback_query_handler(state=AddCarForm.enter_measures, text='km')
async def measures_km(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['measures'] = 'km'
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        f"Enter description for {data['model']} {data['model_name']}",
        reply_markup=ikb_no_description_menu
    )


@dp.callback_query_handler(state=AddCarForm.enter_measures, text='miles')
async def measures_miles(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['measures'] = 'miles'
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await call.message.answer(
        f"Enter description for {data['model']} {data['model_name']}",
        reply_markup=ikb_no_description_menu
    )


@dp.message_handler(state=AddCarForm.enter_measures)
async def enter_measures(message: types.Message, state: FSMContext):
    try:
        mes = message.text.replace(" ", "").translate(str.maketrans('', '', string.punctuation))
        if Car.is_km_or_miles(mes):
            return await message.reply('Enter a valid mileage', reply_markup=ikb_km_m_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid mileage', reply_markup=ikb_km_m_menu)

    async with state.proxy() as data:
        data['measures'] = mes
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await message.answer(
        f"Enter description for {data['model']} {data['model_name']}",
        reply_markup=ikb_no_description_menu
    )


@dp.message_handler(state=AddCarForm.enter_description)
async def enter_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    try:
        db_auto.add_car(*vars(Car(
            data['model'],
            data['model_name'],
            data['mileage'],
            data['measures'],
            data['date_added'],
            data['description'],
        )).values())
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')

    await message.answer(f"{data['model']} {data['model_name']} added at {data['date_added']}",
                         reply_markup=ikb_menu)
    await state.finish()


@dp.callback_query_handler(state=AddCarForm.enter_description, text='no_description')
async def no_description(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = ''
    try:
        db_auto.add_car(*vars(Car(
            data['model'],
            data['model_name'],
            data['mileage'],
            data['measures'],
            data['date_added'],
            data['description'],
        )).values())
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')

    await call.message.answer(f"{data['model']} {data['model_name']} added at {data['date_added']}",
                              reply_markup=ikb_menu)
    await state.finish()
