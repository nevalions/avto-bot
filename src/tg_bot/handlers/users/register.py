import logging.config
from aiogram import types

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from loader import dp
from tg_bot.keybords.inline import ikb_cancel_menu, ikb_menu

from classes import User

from db import AutoBotTgUsersDB, AutoBotMainDB, AutoBotUserDB

from log_dir.log_conf import LOGGING_CONFIG
from log_dir.func_auto_log import autolog_warning, autolog_info

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db_user = AutoBotUserDB()
db_tg_users = AutoBotTgUsersDB()
db_main = AutoBotMainDB()


class RegisterForm(StatesGroup):
    enter_username = State()
    enter_email = State()


@dp.callback_query_handler(text='register')
async def register_command_inline(call: CallbackQuery, state: FSMContext):
    autolog_info(f'Telegram register user started {call.message.chat.id}')
    async with state.proxy() as data:
        data['tg_user_id'] = call.message.from_user.id
        data['chat_id'] = call.message.chat.id
    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', data['chat_id'])
        db_main.close()
        if is_registered[0]['fk_tg_users_users']:
            autolog_warning(f'Telegram user {call.message.chat.id} already registered')
            await call.message.answer('You are already registered', reply_markup=ikb_menu)
            await state.finish()
        else:
            await RegisterForm.enter_username.set()
            await call.message.answer(
                f'Please, enter your username in our service.', reply_markup=ikb_cancel_menu
            )
    except Exception as ex:
        logging.error(ex)


@dp.callback_query_handler(state='*', text='cancel')
async def register_command_inline(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await call.message.answer(
        'Cancelled.', reply_markup=types.ReplyKeyboardRemove()
    )


# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     await state.finish()
#     # And remove keyboard (just in case)
#     await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=RegisterForm.enter_username)
async def register_username(message: types.Message, state: FSMContext):
    autolog_info(f'User entered username "{message.text}"')
    try:
        if User.not_empty_str(message.text):
            return await message.reply('Enter a valid username', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply('Enter a valid username', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['username'] = message.text

    await RegisterForm.enter_email.set()
    await message.answer(f"Enter email for user {message.text}", reply_markup=ikb_cancel_menu)


@dp.message_handler(state=RegisterForm.enter_email)
async def register_email(message: types.Message, state: FSMContext):
    autolog_info(f'User entered email "{message.text}"')
    try:
        if User.check_email(message.text):
            autolog_warning('Enter a valid email')
            return await message.reply('Enter a valid email', reply_markup=ikb_cancel_menu)
        elif db_user.search_user_email_in_db('email', message.text):
            autolog_warning('Email already exist.\n Enter a valid email')
            return await message.reply(f'Email already exist.\n Enter a valid email', reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply('Enter a valid email', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['email'] = message.text
    try:
        new_user = User(data['username'], data['email'])
        tg_referer_id = db_user.add_user(*vars(new_user).values())
        autolog_warning(f"User added to DB {data['username']}, {data['email']}")

        async with state.proxy() as data:
            data['fk_tg_user_id'] = tg_referer_id

        autolog_warning(f"Users_tg_users relation added {data['tg_user_id']}, {data['fk_tg_user_id']}, {data['chat_id']}")
        db_tg_users.add_tg_user_register(int(data['tg_user_id']), int(data['fk_tg_user_id']), int(data['chat_id']))

        await state.finish()
    except Exception as ex:
        logging.error(ex)

    await message.answer(f"User {data['username']} with email: {data['email']} registered", reply_markup=ikb_menu)
    await state.finish()
