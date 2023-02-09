async def on_startup(_dp):

    # from utils.notify_admins import on_startup_notify
    # await on_startup_notify(_dp)


    from utils.set_bot_commands import set_default_commands
    await set_default_commands(_dp)

    print('Bot started')

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
