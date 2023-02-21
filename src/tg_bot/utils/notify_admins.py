from aiogram import Dispatcher

from src.config_tg import admins_id


async def on_startup_notify(dp: Dispatcher):

    for admin in admins_id:
        try:
            text = 'Bot AutoBot started'
            await dp.bot.send_message(chat_id=admin, text=text)
        except Exception as ex:
            print(ex)
            print('Admin send error')
