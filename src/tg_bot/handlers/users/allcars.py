import logging.config

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_menu, show_delete_cars_menu, \
    show_all_cars_menu, car_action_menu_cd, show_cars_cancel_menu

from async_db.base import DATABASE_URL, Database
from async_db.tg_users import TgUserService
from async_db.cars import CarService
from tg_bot.keybords.inline import ikb_cancel_menu

from src.classes import Car

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

db = Database(DATABASE_URL)
tg_user_service = TgUserService(db)
car_service = CarService(db)


class UpdateCarForm(StatesGroup):
    car_id = State()
    car_model = State()


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    autolog_info(f"Show all user's cars")
    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(int(call.message.chat.id))
        if is_registered.tg_users_id is not None:
            autolog_info(f"Show all tg_user {call.message.chat.id} cars")
            user_id = is_registered.fk_users
            user_cars = await car_service.get_all_user_cars(user_id)
            if user_cars:
                autolog_info(f"tg_user {call.message.chat.id} have some cars")
                for car in user_cars:
                    await call.message.answer(
                        f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                        reply_markup=show_all_cars_menu(car['id'])
                    )
            else:
                autolog_warning(f"tg_user {call.message.chat.id} don't have any car")
                await call.message.answer("You don't have any car", reply_markup=ikb_menu)
        else:
            await call.message.answer("You don't have any car", reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(car_action_menu_cd.filter(action='cancel'), state='*')
async def cancel_car_action(query: CallbackQuery, callback_data: dict, state: FSMContext):
    current_state = await state.get_state()
    autolog_warning(f'User canceled car id({callback_data["car_id"]}) action')
    if current_state is None:
        return

    await state.finish()
    await query.message.answer(
        f'Action cancelled.', reply_markup=ikb_menu
    )


@dp.callback_query_handler(car_action_menu_cd.filter(action='edit_model'))
async def update_inline_car_model(query: CallbackQuery, callback_data: dict, state: FSMContext):
    autolog_info(f"Edit car id {callback_data['car_id']} model")

    async with state.proxy() as data:
        data['car_id'] = callback_data['car_id']
    await UpdateCarForm.car_model.set()

    await query.message.answer(f'Enter new model', reply_markup=show_cars_cancel_menu(callback_data['car_id']))


@dp.message_handler(state=UpdateCarForm.car_model)
async def enter_model(message: Message, state: FSMContext):
    autolog_info(f"Enter new car value")
    try:
        if Car.not_empty_str(message.text):
            autolog_warning(f'Invalid car model "{message.text}"')
            return await message.reply(f'Invalid car model "{message.text}"\n'
                                       f'Enter a valid model', reply_markup=ikb_cancel_menu)

        async with state.proxy() as data:
            data['car_model'] = message.text
            await car_service.update_car_model(int(data['car_id']), data['car_model'])
            await message.answer('Car updated', reply_markup=ikb_menu)

    except Exception as ex:
        logging.error(ex)
        return await message.reply(f'Invalid car model"{message.text}"\n'
                                   f'Enter a valid model', reply_markup=ikb_cancel_menu)
    finally:
        await state.finish()
        await db.engine.dispose()


# edit_model_name


@dp.callback_query_handler(car_action_menu_cd.filter(action='delete'))
async def delete_inline_car(query: CallbackQuery, callback_data: dict):
    autolog_info(f"Delete car ask")
    markup = await show_delete_cars_menu(callback_data['car_id'])
    await query.message.answer(f'Are you sure you want to delete {callback_data["car_id"]}', reply_markup=markup)


@dp.callback_query_handler(car_action_menu_cd.filter(action='delete_ok'))
async def delete_car_ok(query: CallbackQuery, callback_data: dict):
    autolog_info(f"Delete car ok")
    await car_service.delete_car(int(callback_data['car_id']))
    await db.engine.dispose()
    await query.message.answer(f'Car deleted', reply_markup=ikb_menu)
