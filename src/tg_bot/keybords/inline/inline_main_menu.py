from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb_start_menu = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[
                                          [
                                              InlineKeyboardButton(text='Register',
                                                                   callback_data='register')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Add new car',
                                                                   callback_data='addcar')
                                          ],
                                          [
                                              InlineKeyboardButton(text='Show your cars',
                                                                   callback_data='allcars')
                                          ]
                                      ])

ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Add new car',
                                                             callback_data='addcar')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Show your cars',
                                                             callback_data='allcars')
                                    ]
                                ])

ikb_cancel_menu = InlineKeyboardMarkup(row_width=1,
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text='Cancel',
                                                                    callback_data='cancel')
                                           ],
                                       ])

ikb_no_description_menu = InlineKeyboardMarkup(row_width=1,
                                               inline_keyboard=[
                                                   [
                                                       InlineKeyboardButton(text='No Description',
                                                                            callback_data='no_description'),
                                                   ],
                                               ])

ikb_km_m_menu = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text='Km',
                                                                  callback_data='km'),
                                             InlineKeyboardButton(text='Miles',
                                                                  callback_data='miles')
                                         ],
                                     ])

ikb_car_add = InlineKeyboardMarkup(row_width=1,
                                   inline_keyboard=[
                                       [
                                           InlineKeyboardButton(text='Add new car',
                                                                callback_data='addcar')]
                                   ])
