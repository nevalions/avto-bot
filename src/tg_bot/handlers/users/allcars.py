from aiogram import types
from aiogram.types import CallbackQuery

from src.tg_bot.loader import dp

from db_main_helper import AutoBotMainDB
from src.tg_bot.keybords.inline import ikb_car_menu, ikb_menu

db_main = AutoBotMainDB()


@dp.message_handler(commands=['allcars'])
async def register_command(message: types.Message):
    try:
        user_cars = db_main.show_all_users_cars(15)
        for car in user_cars:
            await message.answer(
                f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}"
            )
        await message.answer('Menu', reply_markup=ikb_menu)
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')


@dp.callback_query_handler(text='allcars')
async def register_command_inline(call: CallbackQuery):
    try:
        user_cars = db_main.show_all_users_cars(15)
        for car in user_cars:
            await call.message.answer(
                f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}",
                reply_markup=ikb_car_menu
            )
        await call.message.answer('Menu', reply_markup=ikb_menu)
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')
