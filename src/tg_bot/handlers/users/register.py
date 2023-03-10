import logging.config

from aiogram import types

from src.async_db.base import DATABASE_URL, Database
from src.async_db.tg_users import TgUserService
from src.async_db.users import UserService

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_cancel_menu, ikb_menu

from src.classes import User

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


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
        db = Database(DATABASE_URL)
        tg_user_service = TgUserService(db)

        is_registered = await tg_user_service.get_tg_user_by_chat_id(data['chat_id'])
        await db.engine.dispose()

        if is_registered.fk_user:
            autolog_warning(f'Telegram user {call.message.chat.id} already registered')
            await call.message.answer(
                'You are already registered',
                reply_markup=ikb_menu)
            await state.finish()
        else:
            await RegisterForm.enter_username.set()
            await call.message.answer(
                f'Please, enter your username in our service.',
                reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_register(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

    await call.message.answer(
        'Cancelled.',
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(state=RegisterForm.enter_username)
async def register_username(message: types.Message, state: FSMContext):
    autolog_info(f'User entered username "{message.text}"')
    try:
        if User.not_empty_str(message.text):
            return await message.reply(
                'Enter a valid username',
                reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply(
            'Enter a valid username',
            reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['username'] = message.text

    await RegisterForm.enter_email.set()
    await message.answer(
        f"Enter email for user {message.text}",
        reply_markup=ikb_cancel_menu)


@dp.message_handler(state=RegisterForm.enter_email)
async def register_email(message: types.Message, state: FSMContext):
    autolog_info(f'User entered email "{message.text}"')
    db = Database(DATABASE_URL)
    user_service = UserService(db)
    tg_user_service = TgUserService(db)
    user = await user_service.get_user_by_email(message.text)

    try:
        if User.check_email(message.text):
            autolog_warning('Enter a valid email')
            return await message.reply(
                'Enter a valid email',
                reply_markup=ikb_cancel_menu)
        elif user:
            autolog_warning(f'Email {user.email} already exist.\n Enter a valid email')
            return await message.reply(
                f'Email already exist.\n Enter a valid email',
                reply_markup=ikb_cancel_menu)
    except Exception as ex:
        logging.error(ex)
        return await message.reply('Enter a valid email', reply_markup=ikb_cancel_menu)

    async with state.proxy() as data:
        data['email'] = message.text
    try:
        tg_referer_id = await user_service.add_user(data['username'], data['email'])
        autolog_warning(f"User added to DB {data['username']}, {data['email']}")

        async with state.proxy() as data:
            data['fk_tg_user_id'] = tg_referer_id.id

        autolog_warning(
            f"User_tg_user relation added {data['tg_user_id']}, {data['fk_tg_user_id']}, {data['chat_id']}")
        await tg_user_service.add_tg_user_register(
            int(data['tg_user_id']),
            int(data['fk_tg_user_id']),
            int(data['chat_id'])
        )
        await db.engine.dispose()

        await state.finish()
    except Exception as ex:
        logging.error(ex)

    await message.answer(f"User {data['username']} with email: {data['email']} registered", reply_markup=ikb_menu)
    await state.finish()
    await db.engine.dispose()
