from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from src.tg_bot.loader import dp

from users import User

from db_user_helper import AutoBotUserDB
db_user = AutoBotUserDB()


class RegisterForm(StatesGroup):
    enter_username = State()
    enter_email = State()


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
        new_user = User(data['username'], data['email'])
        print(*vars(new_user).values())
        db_user.add_user(*vars(new_user).values())
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')

    await message.answer(f"User {data['username']} with email: {data['email']} registered")
    await state.finish()
