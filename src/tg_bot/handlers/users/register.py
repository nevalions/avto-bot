from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

from src.tg_bot.loader import dp
from tg_bot.keybords.inline import ikb_cancel_menu

from users import User

from db_user_helper import AutoBotUserDB
from db_tg_users import AutoBotTgUsersDB

db_user = AutoBotUserDB()
db_tg_users = AutoBotTgUsersDB()


class RegisterForm(StatesGroup):
    enter_username = State()
    enter_email = State()


@dp.callback_query_handler(text='register')
async def register_command_inline(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['tg_user_id'] = call.message.from_user.id
        data['chat_id'] = call.message.chat.id
    await RegisterForm.enter_username.set()
    await call.message.answer(
        f'Please, enter your username in our service.', reply_markup=ikb_cancel_menu
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


@dp.message_handler(state=RegisterForm.enter_username)
async def register_username(message: types.Message, state: FSMContext):

    try:
        if User.not_empty_str(message.text):
            return await message.reply('Enter a valid username', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid username', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['username'] = message.text

    await RegisterForm.enter_email.set()
    await message.answer(f"Enter email for user {message.text}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=RegisterForm.enter_email)
async def register_email(message: types.Message, state: FSMContext):
    try:
        if User.check_email(message.text):
            return await message.reply('Enter a valid email', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        print(ex)
        return await message.reply('Enter a valid email', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['email'] = message.text
    try:
        new_user = User(data['username'], data['email'])
        print(*vars(new_user).values())
        tg_referer_id = db_user.add_user(*vars(new_user).values())

        async with state.proxy() as data:
            data['fk_tg_user_id'] = tg_referer_id

        print(data['tg_user_id'], data['fk_tg_user_id'], data['chat_id'])
        db_tg_users.add_tg_user_register(int(data['tg_user_id']), int(data['fk_tg_user_id']), int(data['chat_id']))

        print(data['chat_id'])
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')

    await message.answer(f"User {data['username']} with email: {data['email']} registered")
    await state.finish()
