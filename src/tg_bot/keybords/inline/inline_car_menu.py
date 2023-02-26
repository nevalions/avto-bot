from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_car_menu = InlineKeyboardMarkup(row_width=2,
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
                                                                 callback_data='car_menu_delete')
                                        ]
                                    ])


