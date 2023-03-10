from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from src.tg_bot.keybords.inline import car_action_menu_cd, maintenance_action_menu_cd

from src.tg_bot.handlers.users.menu_text_helper import MenuText, cancel_txt, delete_txt

work_action_menu_cd = CallbackData(
    'action_menu_cd',
    'action',
    'work_id',
    'maintenance_id'
)


def make_work_callback_data(action, work_id=None, maintenance_id=None):
    return work_action_menu_cd.new(action=action,
                                   work_id=work_id,
                                   maintenance_id=maintenance_id)


def show_all_works_menu(work_id=None, maintenance_id=None):
    ikb_work_menu_i = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(text=MenuText.show_top_works(),
                                     callback_data='works-top')
            ],
            [
                InlineKeyboardButton(text='-',
                                     callback_data=work_action_menu_cd.new(
                                         action='spacer',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text=MenuText.edit_work_title(),
                                     callback_data=work_action_menu_cd.new(
                                         action='edit_work_title',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     ),
                InlineKeyboardButton(text=MenuText.edit_work_description(),
                                     callback_data=work_action_menu_cd.new(
                                         action='edit_work_description',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text=MenuText.edit_work_is_regular(),
                                     callback_data=work_action_menu_cd.new(
                                         action='edit_work_is_regular',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text=MenuText.edit_next_maintenance_mileage(),
                                     callback_data=work_action_menu_cd.new(
                                         action='edit_next_maintenance_mileage',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ],
            [
                InlineKeyboardButton(text=delete_txt,
                                     callback_data=work_action_menu_cd.new(
                                         action='delete_work',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ],
        ])
    return ikb_work_menu_i


def add_new_work(work_id=None, maintenance_id=None):
    ikb_maintenance_add_menu_i = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Add Work',
                                     callback_data=work_action_menu_cd.new(
                                         action='add_work',
                                         work_id=work_id,
                                         maintenance_id=maintenance_id
                                     )
                                     )
            ]
        ]
    )
    return ikb_maintenance_add_menu_i

#
# def add_new_maintenance(maintenance_id=None, car_id=None):
#     ikb_maintenance_add_menu_i = InlineKeyboardMarkup(
#         row_width=1,
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=MenuText.add_maintenance(),
#                                      callback_data=maintenance_action_menu_cd.new(
#                                          action='add_car_maintenances',
#                                          maintenance_id=maintenance_id,
#                                          car_id=car_id)
#                                      )
#             ]
#         ]
#     )
#     return ikb_maintenance_add_menu_i
#
#
# def show_all_maintenance_one_btn(car_id=None):
#     show_all_maintenance_one_btn_i = InlineKeyboardMarkup(
#         row_width=1,
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=MenuText.show_maintenances(),
#                                      callback_data=car_action_menu_cd.new(
#                                          action='show_car_maintenances',
#                                          car_id=car_id)
#                                      )
#             ]
#         ]
#     )
#     return show_all_maintenance_one_btn_i
#
#
# def show_maintenance_cancel_menu(maintenance_id=None, car_id=None):
#     ikb_maintenance_cancel_menu = InlineKeyboardMarkup(
#         row_width=1,
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=cancel_txt,
#                                      callback_data=maintenance_action_menu_cd.new(
#                                          action='cancel',
#                                          maintenance_id=maintenance_id,
#                                          car_id=car_id)
#                                      )
#             ],
#         ])
#     return ikb_maintenance_cancel_menu
#
#
# async def show_delete_maintenance_menu(maintenance_id=None, car_id=None):
#     delete_maintenance_menu = InlineKeyboardMarkup(
#         row_width=2,
#         inline_keyboard=[
#             [
#                 InlineKeyboardButton(text=delete_txt,
#                                      callback_data=maintenance_action_menu_cd.new(
#                                          action='delete_maintenance_ok',
#                                          maintenance_id=maintenance_id,
#                                          car_id=car_id
#                                          )
#                                      ),
#                 InlineKeyboardButton(text=cancel_txt,
#                                      callback_data=maintenance_action_menu_cd.new(
#                                          action='cancel_delete_maintenance',
#                                          maintenance_id=maintenance_id,
#                                          car_id=car_id
#                                          )
#                                      )
#             ]
#         ])
#     return delete_maintenance_menu
