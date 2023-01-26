from aiogram import types

from src.tg_bot.loader import dp

from db_main_helper import AutoBotMainDB
db_main = AutoBotMainDB()


@dp.message_handler(commands=['allcars'])
async def register_command(message: types.Message):
    try:
        user_cars = db_main.show_all_users_cars(15)
        for car in user_cars:
            await message.answer(
                f"ID({car['id']}) {car['model']} {car['model_name']} with {car['mileage']} {car['measures']}"
            )
        await message.answer('If you want to edit your car, enter /editcar')
    except Exception as ex:
        print(ex)
        print('Error connecting to DB')
