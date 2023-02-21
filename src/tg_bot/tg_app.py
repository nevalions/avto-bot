async def on_startup(_dp):

    # from utils.notify_admins import on_startup_notify
    # await on_startup_notify(_dp)

    from src.tg_bot.utils.set_bot_commands import set_default_commands
    await set_default_commands(_dp)

    print('Bot started')


def start_bot():
    from aiogram import executor
    from src.tg_bot.handlers import dp

    executor.start_polling(dp, on_startup=on_startup)


start_bot()
