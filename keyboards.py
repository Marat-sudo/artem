
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



def answer(product_id):
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("положить товар в корзину", callback_data='answer_products_Yes_' + str(product_id))
    b2 = types.InlineKeyboardButton("выбрать другой товар", callback_data='answer_products_No' + str(product_id))
    kbd.add(b1, b2)
    return kbd

def basket(id, page=0):
    head, values = fc.all_products_from_basket(id, page)
    """
    ----------------------------------------------------------------------------------------------------
(1, 1, 'new', 694.5, '2025-12-15 14:43:51') [(3, 1, 217.3, 217.3), (6, 1, 57.0, 57.0), (9, 3, 105.4, 316.20000000000005), (13, 1, 104.0, 104.0), ('cat', 'пусто'), ('cat', 'пусто')]
[(3, 1,  217.3, 217.3), (6, 1, 57.0, 57.0), (9, 3, 105.4, 316.20000000000005), (13, 1, 104.0, 104.0)]
  смотри в бд
    """

    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(values[0][-1], callback_data='basket_' + str(values[0][0]))
    b2 = types.InlineKeyboardButton(values[1][-1], callback_data='basket_' + str(values[1][0]))
    b3 = types.InlineKeyboardButton(values[2][-1], callback_data='basket_' + str(values[2][0]))
    b4 = types.InlineKeyboardButton(values[3][-1], callback_data='basket_' + str(values[3][0]))
    b5 = types.InlineKeyboardButton(values[4][-1], callback_data='basket_' + str(values[4][0]))
    b6 = types.InlineKeyboardButton(values[5][-1], callback_data='basket_' + str(values[5][0]))
    b7 = types.InlineKeyboardButton("<", callback_data='basket_page_-1_' + str(page))
    b8 = types.InlineKeyboardButton("назад", callback_data='page_cat')
    b9 = types.InlineKeyboardButton(">", callback_data='basket_page_+1_' + str(page))
    kbd.add(b1, b2, b3, b4, b5, b6)
    kbd.row(b7, b8, b9)
    return kbd