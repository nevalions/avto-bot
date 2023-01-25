import string
from datetime import datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from config_tg import tg_token


from users import User
from cars import Car
from db_user_helper import AutoBotUserDB
from db_auto_helper import AutoBotAutoDB
from db_main_helper import AutoBotMainDB


bot = Bot(token=tg_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_user = AutoBotUserDB()
db_auto = AutoBotAutoDB()

now = datetime.now()


def main():
    executor.start_polling(dp)


class RegisterForm(StatesGroup):
    enter_username = State()
    enter_email = State()


class AddCarForm(StatesGroup):
    enter_model = State()
    enter_model_name = State()
    enter_mileage = State()
    enter_measures = State()
    enter_description = State()


@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    """
    Telegram bot with aiogram.
    Register user.
    User can create cars with model, model name,
    mileage and description.
    """
    # say hello to user and get tg.id
    print(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await message.answer(
        f'Hi, {message.from_user.first_name} {message.from_user.last_name}!\n'
        f'If you want to use AutoBot /register first\n'
        f'If you are already registered you can /addcar'
    )


@dp.message_handler(commands=['register'])
async def register_command(message: types.Message):
    await RegisterForm.enter_username.set()
    await message.answer(
        f'Please, enter your username in our service.'
    )


@dp.message_handler(state=RegisterForm.enter_username)
async def register_username(message: types.Message, state: FSMContext):

    try:
        if User.not_empty_str(message.text):
            return await message.reply('Enter a valid username')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid username')

    async with state.proxy() as data:
        data['username'] = message.text

    await RegisterForm.enter_email.set()
    await message.answer(f"Enter email for user {message.text}")


@dp.message_handler(state=RegisterForm.enter_email)
async def register_email(message: types.Message, state: FSMContext):
    try:
        if User.check_email(message.text):
            return await message.reply('Enter a valid email')
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid email')

    async with state.proxy() as data:
        data['email'] = message.text
    try:
        db_user.add_user(*vars(User(data['username'], data['email'])).values())
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')

    await message.answer(f"User {data['username']} with email: {data['email']} registered")
    await state.finish()


@dp.message_handler(commands=['addcar'])
async def addcar_command(message: types.Message):
    await AddCarForm.enter_model.set()
    await message.answer(
        f'Please, enter car model (Lada, Ford, Chevrolet, etc)'
    )


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
async def enter_model_name(message: types.Message, state: FSMContext):

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
async def enter_model_name(message: types.Message, state: FSMContext):

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
async def enter_model_name(message: types.Message, state: FSMContext):
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

if __name__ == '__main__':
    main()
