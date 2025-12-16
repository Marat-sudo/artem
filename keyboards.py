
from telebot import types
import db
import any_func as fc

def start_kd():
    kbd = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    b1 = types.KeyboardButton("/reg")
    b2 = types.KeyboardButton("/basket")
    b3 = types.KeyboardButton("/catalog")
    kbd.add(b1, b2, b3)
    return kbd


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
    size = str(page + 1) + "/" + str(db.catalog_size() // 6 + 1)
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(products[0][1], callback_data='products_' + str(products[0][0]))
    b2 = types.InlineKeyboardButton(products[1][1], callback_data='products_' + str(products[1][0]))
    b3 = types.InlineKeyboardButton(products[2][1], callback_data='products_' + str(products[2][0]))
    b4 = types.InlineKeyboardButton(products[3][1], callback_data='products_' + str(products[3][0]))
    b5 = types.InlineKeyboardButton(products[4][1], callback_data='products_' + str(products[4][0]))
    b6 = types.InlineKeyboardButton(products[5][1], callback_data='products_' + str(products[5][0]))
    b7 = types.InlineKeyboardButton("<", callback_data='page_-1_' + str(page))
    b8 = types.InlineKeyboardButton(size, callback_data='another')
    b9 = types.InlineKeyboardButton(">", callback_data='page_+1_' + str(page))
    b10 = types.InlineKeyboardButton("корзина", callback_data='back_products')
    kbd.add(b1, b2, b3, b4, b5, b6)
    kbd.row(b7, b8, b9)
    kbd.add(b10)
    return kbd



def answer(product_id):
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("положить товар в корзину", callback_data='answer_products_Yes_' + str(product_id))
    b2 = types.InlineKeyboardButton("выбрать другой товар", callback_data='answer_products_No' + str(product_id))
    kbd.add(b1, b2)
    return kbd

def basket(tg_id, page=0):
    values = fc.all_products_from_basket(tg_id, page)
    size = str(page + 1) + "/" + str(db.basket_size(tg_id) // 6 + 1)
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton(values[0][-1] + f" {str(values[0][1])}шт", callback_data='basket_item_' + str(values[0][0]))
    b2 = types.InlineKeyboardButton(values[1][-1] + f" {str(values[1][1])}шт", callback_data='basket_item_' + str(values[1][0]))
    b3 = types.InlineKeyboardButton(values[2][-1] + f" {str(values[2][1])}шт", callback_data='basket_item_' + str(values[2][0]))
    b4 = types.InlineKeyboardButton(values[3][-1] + f" {str(values[3][1])}шт", callback_data='basket_item_' + str(values[3][0]))
    b5 = types.InlineKeyboardButton(values[4][-1] + f" {str(values[4][1])}шт", callback_data='basket_item_' + str(values[4][0]))
    b6 = types.InlineKeyboardButton(values[5][-1] + f" {str(values[5][1])}шт", callback_data='basket_item_' + str(values[5][0]))
    b7 = types.InlineKeyboardButton("<", callback_data='basket_page_-1_' + str(page))
    b8 = types.InlineKeyboardButton(size, callback_data='another')
    b9 = types.InlineKeyboardButton(">", callback_data='basket_page_+1_' + str(page))
    b10 = types.InlineKeyboardButton("оплата корзины", callback_data='pay')
    b11 = types.InlineKeyboardButton("каталог", callback_data='back_basket')
    kbd.add(b1, b2, b3, b4, b5, b6)
    kbd.add(b10)
    kbd.add(b11)
    kbd.row(b7, b8, b9)
    
    return kbd


def item_choice(product_id: str):
    kbd = types.InlineKeyboardMarkup(row_width=2)
    b1 = types.InlineKeyboardButton("удалить один товар", callback_data='choice_answer_one_' + product_id)
    b2 = types.InlineKeyboardButton("удалить весь товар", callback_data='choice_answer_all_' + product_id)
    b3 = types.InlineKeyboardButton("вернутся назад", callback_data='back_choice')
    kbd.add(b1, b2)
    kbd.row(b3)
    return kbd