from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.tg_bot.handlers.users.menu_text_helper import MenuText, cancel_txt

add_car_text = MenuText.main_menu()["add_car"]

ikb_start_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=MenuText.register(),
                                 callback_data='register')
        ]
    ])

ikb_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=add_car_text,
                                 callback_data='addcar')
        ],
        [
            InlineKeyboardButton(text=MenuText.main_menu()["show_cars"],
                                 callback_data='allcars')
        ]
    ])

ikb_cancel_menu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=cancel_txt,
                                 callback_data='cancel')
        ],
    ])

ikb_no_description_menu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=MenuText.no_description(),
                callback_data='no_description'),
        ],
    ])

ikb_km_m_menu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text='KM',
                                 callback_data='km'),
            InlineKeyboardButton(text='MILES',
                                 callback_data='miles')
        ],
    ])

ikb_car_add = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=add_car_text,
                                 callback_data='addcar')]
    ])
