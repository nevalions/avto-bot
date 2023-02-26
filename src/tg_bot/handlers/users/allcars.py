import logging.config
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from src.logs.log_conf_main import LOGGING_CONFIG
from src.logs.func_auto_log import autolog_warning, autolog_info

from src.tg_bot.loader import dp
from src.tg_bot.keybords.inline import ikb_car_menu, ikb_menu

from async_db.base import DATABASE_URL, Database
from async_db.tg_users import TgUserService
from async_db.cars import CarService

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

menu_cd = CallbackData('menu', 'id')


def make_callback_data(item_id):
    return menu_cd.new(menu='car_menu_delete', id=item_id)


async def show_delete_cars_menu():
    markup = InlineKeyboardMarkup(row_width=2)

    callback_data = make_callback_data(item_id=1)

    markup.insert(
        InlineKeyboardButton(text='text', callback_data=callback_data)
    )

    return markup

# def delete_car_menu(id):
#     ikb_delete_car_menu = InlineKeyboardMarkup(row_width=2,
#                                                inline_keyboard=[
#                                                    [
#                                                        InlineKeyboardButton(text='DELETE',
#                                                                             callback_data=f'delete_ok_final {id}')
#                                                    ],
#                                                    [
#                                                        InlineKeyboardButton(text='Cancel',
#                                                                             callback_data='cancel')
#                                                    ]
#                                                ])
#     return ikb_delete_car_menu


# def show_all_cars_menu():
#     ikb_car_menu_i = InlineKeyboardMarkup(row_width=2,
#                                           inline_keyboard=[
#                                               [
#                                                   InlineKeyboardButton(text='Edit model',
#                                                                        callback_data='edit_model'),
#                                                   InlineKeyboardButton(text='Edit model name',
#                                                                        callback_data='edit_model_name')
#                                               ],
#                                               [
#                                                   InlineKeyboardButton(text='Add current mileage',
#                                                                        callback_data='add_cur_mil')
#                                               ],
#                                               [
#                                                   InlineKeyboardButton(text='Add TO',
#                                                                        callback_data='to')
#                                               ],
#                                               [
#                                                   InlineKeyboardButton(text='DELETE CAR',
#                                                                        callback_data='car_menu_delete')
#                                               ]
#                                           ])
#     return ikb_car_menu_i


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    autolog_info(f"Show all user's cars")

    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)
    car_service = CarService(db)

    try:
        is_registered = await tg_user_service.get_tg_user_by_chat_id(int(call.message.chat.id))
        if is_registered.tg_users_id is not None:
            autolog_info(f"Show all tg_user {call.message.chat.id} cars")
            user_id = is_registered.fk_users
            user_cars = await car_service.get_all_user_cars(user_id)
            # markup = await show_all_cars_menu()
            # print(markup)
            if user_cars:
                autolog_info(f"tg_user {call.message.chat.id} have some cars")
                for car in user_cars:
                    await call.message.answer(
                        f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                        reply_markup=ikb_car_menu
                    )
                await call.message.answer('Please select from menu', reply_markup=ikb_menu)
                # return car
            else:
                autolog_warning(f"tg_user {call.message.chat.id} don't have any car")
                await call.message.answer("You don't have any car", reply_markup=ikb_menu)
        else:
            await call.message.answer("You don't have any car", reply_markup=ikb_menu)
    except Exception as ex:
        logging.error(ex)
    finally:
        await db.engine.dispose()


@dp.callback_query_handler(menu_cd.filter())
async def delete_inline_car(call: CallbackQuery, callback_data: dict):
    autolog_info(f"Delete car")
    markup = await show_delete_cars_menu()
    await call.message.answer(f'Are you sure you want to delete', reply_markup=markup)
    # , reply_markup = delete_car_menu()
