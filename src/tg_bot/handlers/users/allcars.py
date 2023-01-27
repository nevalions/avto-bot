from aiogram import types
from aiogram.types import CallbackQuery

from src.tg_bot.loader import dp

from src.tg_bot.keybords.inline import ikb_car_menu, ikb_menu

from db_main_helper import AutoBotMainDB
from db_tg_users import AutoBotTgUsersDB

db_main = AutoBotMainDB()
db_tg_users = AutoBotTgUsersDB()


@dp.callback_query_handler(text='allcars')
async def show_users_cars(call: CallbackQuery):
    chat_id = call.message.chat.id
    try:
        is_registered = db_tg_users.search_tg_user_chat_id_in_db('chat_id', call.message.chat.id)
        if is_registered[0]['fk_tg_users_users'] is not None:
            user_id = is_registered[0]['fk_tg_users_users']
            user_cars = db_main.show_all_users_cars(user_id)
            for car in user_cars:
                await call.message.answer(
                    f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                    reply_markup=ikb_car_menu
                )
            await call.message.answer('Please select from menu', reply_markup=ikb_menu)
        else:
            await call.message.answer("You don't have any car", reply_markup=ikb_menu)
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')
