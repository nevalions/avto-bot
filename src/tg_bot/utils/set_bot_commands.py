from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('menu', 'Show menu')
        # types.BotCommand('register', 'Register new user'),
        # types.BotCommand('addcar', "Add new user's car"),
        # types.BotCommand('allcars', "Show all user's cars")
    ])
