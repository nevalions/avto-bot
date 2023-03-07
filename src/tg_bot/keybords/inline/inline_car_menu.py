from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

car_action_menu_cd = CallbackData('action_menu_cd', 'action', 'car_id')


def make_car_callback_data(action, car_id):
    return car_action_menu_cd.new(action=action, car_id=car_id)


def show_all_cars_menu(car_id):
    ikb_car_menu_i = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔧 Show car maintenances',
                                     callback_data=car_action_menu_cd.new(
                                         action='show_car_maintenances',
                                         car_id=car_id)
                                     )
            ],
            [
                InlineKeyboardButton(text='-',
                                     callback_data=car_action_menu_cd.new(
                                         action='spacer',
                                         car_id=car_id)
                                     )
            ],
            [
                InlineKeyboardButton(text='Edit car model',
                                     callback_data=car_action_menu_cd.new(
                                         action='edit_car_model',
                                         car_id=car_id)
                                     ),
                InlineKeyboardButton(text='Edit car model name',
                                     callback_data=car_action_menu_cd.new(
                                         action='edit_car_model_name',
                                         car_id=car_id)
                                     )
            ],
            [
                InlineKeyboardButton(text='Add car current mileage',
                                     callback_data=car_action_menu_cd.new(
                                         action='edit_car_current_mileage',
                                         car_id=car_id)
                                     )
            ],
            [
                InlineKeyboardButton(text='Edit car description',
                                     callback_data=car_action_menu_cd.new(
                                         action='edit_car_description',
                                         car_id=car_id)
                                     )
            ],
            [
                InlineKeyboardButton(text='❌ Delete car',
                                     callback_data=car_action_menu_cd.new(
                                         action='delete_car',
                                         car_id=car_id)
                                     )
            ],
        ])
    return ikb_car_menu_i


def show_cars_cancel_menu(car_id):
    ikb_car_cancel_menu = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Cancel',
                                     callback_data=car_action_menu_cd.new(
                                         action='cancel',
                                         car_id=car_id))
            ],
        ])
    return ikb_car_cancel_menu


async def show_delete_cars_menu(car_id):
    delete_car_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='❌ Delete',
                                     callback_data=car_action_menu_cd.new(
                                         action='delete_car_ok',
                                         car_id=car_id)),
                InlineKeyboardButton(text='Cancel',
                                     callback_data=car_action_menu_cd.new(
                                         action='cancel_delete_car',
                                         car_id=car_id))
            ]
        ])
    return delete_car_menu
