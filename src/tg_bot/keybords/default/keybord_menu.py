from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='/register', caption='1')
        ],
        [
            KeyboardButton(text='addcar'),
        ],
        [
            KeyboardButton(text='allcars'),
        ],
    ],
    resize_keyboard=True
)