from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

car_action_menu_cd = CallbackData('action_menu_cd', 'action', 'car_id')


def make_callback_data(action, car_id):
    return car_action_menu_cd.new(action=action, car_id=car_id)


async def show_delete_cars_menu(car_id):
    delete_car_menu = InlineKeyboardMarkup(row_width=2,
                                           inline_keyboard=[
                                               [
                                                   InlineKeyboardButton(text='Delete',
                                                                        callback_data=car_action_menu_cd.new(
                                                                            action='delete_ok', car_id=car_id)),
                                                   InlineKeyboardButton(text='Cancel',
                                                                        callback_data='cancel_delete')
                                               ]
                                           ])
    return delete_car_menu


def show_all_cars_menu(car_id):
    ikb_car_menu_i = InlineKeyboardMarkup(row_width=2,
                                          inline_keyboard=[
                                              [
                                                  InlineKeyboardButton(text='Edit model',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='edit_model', car_id=car_id)
                                                                       ),
                                                  InlineKeyboardButton(text='Edit model name',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='edit_model_name', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Add current mileage',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='edit_current_mileage', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Edit description',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='edit_description', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='-',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='spacer', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Add TO',
                                                                       callback_data='add_to')
                                              ],
                                              [
                                                  InlineKeyboardButton(text='-',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='spacer', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='DELETE CAR',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='delete', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='-',
                                                                       callback_data=car_action_menu_cd.new(
                                                                           action='spacer', car_id=car_id)
                                                                       )
                                              ],
                                              [
                                                  InlineKeyboardButton(text='Add new car',
                                                                       callback_data='addcar')
                                              ],

                                          ])
    return ikb_car_menu_i


def show_cars_cancel_menu(car_id):
    ikb_car_cancel_menu = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(text='Cancel',
                                                                            callback_data=car_action_menu_cd.new(
                                                                                action='cancel', car_id=car_id))
                                                   ],
                                               ])
    return ikb_car_cancel_menu
