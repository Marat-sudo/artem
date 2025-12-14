
from telebot import types
import db
import any_func as fc

def reg_user():
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(f'добавить номер телефона', callback_data='reg_phone')
    b2 = types.InlineKeyboardButton(f'добавить электронную почту', callback_data='reg_email')
    b3 = types.InlineKeyboardButton('возврат назад', callback_data='task_back')
    b4 = types.InlineKeyboardButton('возврат назад', callback_data='task_back')
    b5 = types.InlineKeyboardButton('возврат назад', callback_data='task_back')
    kbd.add(b1, b2)
    kbd.row(b3, b4, b5)

    return kbd


def catalog(page=0):
    products = fc.all_products(page)
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(products[0][1], callback_data='products_' + str(products[0][0]))
    b2 = types.InlineKeyboardButton(products[1][1], callback_data='products_' + str(products[1][0]))
    b3 = types.InlineKeyboardButton(products[2][1], callback_data='products_' + str(products[2][0]))
    b4 = types.InlineKeyboardButton(products[3][1], callback_data='products_' + str(products[3][0]))
    b5 = types.InlineKeyboardButton(products[4][1], callback_data='products_' + str(products[4][0]))
    b6 = types.InlineKeyboardButton(products[5][1], callback_data='products_' + str(products[5][0]))
    b7 = types.InlineKeyboardButton("<", callback_data='page_-1_' + str(page))
    b8 = types.InlineKeyboardButton("назад", callback_data='page_cat')
    b9 = types.InlineKeyboardButton(">", callback_data='page_+1_' + str(page))
    kbd.add(b1, b2, b3, b4, b5, b6)
    kbd.row(b7, b8, b9)
    return kbd



