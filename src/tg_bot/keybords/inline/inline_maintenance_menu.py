from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from src.tg_bot.keybords.inline import car_action_menu_cd

maintenance_action_menu_cd = CallbackData('action_menu_cd', 'action', 'maintenance_id', 'car_id')


def make_maintenance_callback_data(action, maintenance_id=None, car_id=None):
    return maintenance_action_menu_cd.new(action=action, maintenance_id=maintenance_id, car_id=car_id)


async def show_delete_maintenance_menu(maintenance_id):
    delete_maintenance_menu = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Delete',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='delete_ok', maintenance_id=maintenance_id)),
                InlineKeyboardButton(text='Cancel',
                                     callback_data='cancel_delete')
            ]
        ])
    return delete_maintenance_menu


def show_all_car_maintenance_menu(maintenance_id=None, car_id=None):
    ikb_maintenance_menu_i = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Show maintenance works',
                                     callback_data='car_maintenance_works')
            ],
            [
                InlineKeyboardButton(text='-',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='spacer',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='Edit maintenance title',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='edit_maintenance_title',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     ),
                InlineKeyboardButton(text='Edit maintenance description',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='edit_maintenance_description',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='Edit maintenance current mileage',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='edit_maintenance_current_mileage',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='Edit maintenance date',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='edit_maintenance_date',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='DELETE maintenance',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='delete_maintenance',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='-',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='spacer',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text='Show all car maintenance',
                                     callback_data=car_action_menu_cd.new(
                                         action='show_car_maintenances',
                                         car_id=car_id)
                                     )
            ],

        ])
    return ikb_maintenance_menu_i


def add_new_maintenance(maintenance_id=None, car_id=None):
    ikb_maintenance_add_menu_i = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Add new car maintenance',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='add_car_maintenances',
                                         maintenance_id=maintenance_id,
                                         car_id=car_id)
                                     )
            ]
        ]
    )
    return ikb_maintenance_add_menu_i


def show_maintenance_cancel_menu(maintenance_id):
    ikb_maintenance_cancel_menu = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Cancel',
                                     callback_data=maintenance_action_menu_cd.new(
                                         action='cancel', maintenance_id=maintenance_id))
            ],
        ])
    return ikb_maintenance_cancel_menu
