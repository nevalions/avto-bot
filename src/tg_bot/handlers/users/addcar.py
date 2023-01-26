import string
from datetime import datetime
from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from src.tg_bot.loader import dp

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
        f'Please, enter car model (Lada, Ford, Chevrolet, etc)'
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
            return await message.reply('Enter a valid model')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid model')

    async with state.proxy() as data:
        data['model'] = message.text

    await AddCarForm.enter_model_name.set()
    await message.answer(f"Enter model name for {data['model']}")


@dp.message_handler(state=AddCarForm.enter_model_name)
async def enter_model_name(message: types.Message, state: FSMContext):

    try:
        if Car.not_empty_str(message.text):
            return await message.reply('Enter a valid model name')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid model name')

    async with state.proxy() as data:
        data['model_name'] = message.text

    await AddCarForm.enter_mileage.set()
    await message.answer(f"Enter mileage for {data['model']} {data['model_name']}")


@dp.message_handler(state=AddCarForm.enter_mileage)
async def enter_mileage(message: types.Message, state: FSMContext):

    try:
        mil = message.text.replace(" ", "").translate(str.maketrans('', '', string.punctuation))
        if Car.is_digit(mil):
            return await message.reply('Enter a valid mileage')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid mileage')

    async with state.proxy() as data:
        data['mileage'] = mil

    await AddCarForm.enter_measures.set()
    await message.answer(f"Enter measures for mileage count (km/miles)")


@dp.message_handler(state=AddCarForm.enter_measures)
async def enter_measures(message: types.Message, state: FSMContext):

    try:
        mes = message.text.replace(" ", "").translate(str.maketrans('', '', string.punctuation))
        if Car.is_km_or_miles(mes):
            return await message.reply('Enter a valid mileage')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid mileage')

    async with state.proxy() as data:
        data['measures'] = mes
        data['date_added'] = f'{now.strftime("%d.%m.%Y")}'

    await AddCarForm.enter_description.set()
    await message.answer(f"Enter description for {data['model']} {data['model_name']}")


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

    await message.answer(f"{data['model']} {data['model_name']} added at {data['date_added']}")
    await state.finish()
