from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

car_action_menu_cd = CallbackData('action_menu_cd', 'action', 'car_id')


def make_callback_data(action, car_id):
    return car_action_menu_cd.new(action=action, car_id=car_id)


async def show_delete_cars_menu(car_id):
    delete_car_menu = InlineKeyboardMarkup(row_width=2,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text='delete',
                                                                        callback_data=car_action_menu_cd.new(
                                                                            action='delete', car_id=car_id)),
                                                   InlineKeyboardButton(text='cancel',
                                                                        callback_data=car_action_menu_cd.new(
                                                                            action='cancel', car_id=car_id))
                                               ]
                                           ])
    return delete_car_menu


def show_all_cars_menu(car_id):
    ikb_car_menu_i = InlineKeyboardMarkup(row_width=2,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Edit model',
                                                                       callback_data='edit_model'),
                                                  InlineKeyboardButton(text='Edit model name',
                                                                       callback_data='edit_model_name')
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Add current mileage',
                                                                       callback_data='add_cur_mil')
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Add TO',
                                                                       callback_data='to')
                                              ],
                                              [
                                                  InlineKeyboardButton(text='DELETE CAR',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='delete', car_id=car_id))
                                              ]
                                          ])
    return ikb_car_menu_i
#
# ikb_car_menu = InlineKeyboardMarkup(row_width=2,
#                                     inline_keyboard=[
#                                         [
#                                             InlineKeyboardButton(text='Edit model',
#                                                                  callback_data='edit_model'),
#                                             InlineKeyboardButton(text='Edit model name',
#                                                                  callback_data='edit_model_name')
#                                         ],
#                                         [
#                                             InlineKeyboardButton(text='Add current mileage',
#                                                                  callback_data='add_cur_mil')
#                                         ],
#                                         [
#                                             InlineKeyboardButton(text='Add TO',
#                                                                  callback_data='to')
#                                         ],
#                                         [
#                                             InlineKeyboardButton(text='DELETE CAR',
#                                                                  callback_data='delete_menu')
#                                         ]
#                                     ])
#

