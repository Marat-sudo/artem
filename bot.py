
from config import TOKEN
import telebot
from math import ceil
from random import choice
import keyboards as kb
import services as sv
import any_func as fc
import db

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', "help"])   # вызов команды старт
def start(message):
    mes = "бот для аптеки, пока тест ня\n" \
    "/reg - регистрия\n " \
    "/basket - корзина\n " \
    "/history - история покупок\n " \
    "/catalog - каталог товаров \n" \
    "/cat - cat"
    bot.send_message(message.chat.id, mes, reply_markup=kb.start_kd())



@bot.message_handler(commands=['reg'])
def reg(message):
    if db.user_not_reg(message.chat.id):
        user_name = str(message.from_user.first_name) + " " +str(message.from_user.last_name)
        db.register_user(message.chat.id, user_name)
    
    bot.send_message(message.chat.id, "Выберите", reply_markup=kb.reg_user())
    bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['catalog'])
def catalog(message):
    bot.send_message(message.chat.id, "privet", reply_markup=kb.catalog())


@bot.message_handler(commands=['basket'])
def basket(message):
    if not db.basket_is_free(db.select_user_id(message.chat.id)):
        head = db.select_basket_head(message.chat.id)
        bot.send_message(message.chat.id, f"Итоговая сумма: {head[3]}", reply_markup=kb.basket(message.chat.id))
    else:
        bot.send_message(message.chat.id, "Корзина пустая")


@bot.callback_query_handler(func=lambda call: call.data.endswith("cat"))
def call_cat(call):
    cat = choice(['koshka', 'koshka_2', 'komury_A', 'kitten in milk',
                  'catic_mili', 'super_rjaka_demotivator_bot', 'inet', 'komury and komugi'])
    ing = open(f'cats/{cat}.mp4', 'rb')
    bot.send_animation(call.message.chat.id, ing, caption='test')
    ing.close()
    bot.delete_message(call.message.chat.id, call.message.message_id)



@bot.callback_query_handler(func=lambda call: call.data.startswith('products_'))
def products_call(call):
    if db.user_in_db(call.message.chat.id):
        with open('cats/photo_2025-12-04_10-52-31.jpg', 'rb') as photo:
            desc = fc.create_description(call.data[9:])
            bot.send_photo(call.message.chat.id, photo, caption=desc, reply_markup=kb.answer(call.data[9:]))
        bot.delete_message(call.message.chat.id, call.message.message_id)

    else:
        bot.answer_callback_query(call.id, text=f"Сначала вам надо зарегестрироватся камандой /reg", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith('answer_products'))
def answer_products_call(call):
    if call.data.find("Yes") > -1:
        sv.basket(db.select_user_id(call.message.chat.id), call.data[20:])
        bot.answer_callback_query(call.id, text=f"Товар {db.select_name_from_id(call.data[20:])} добавлен в корзину", show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog())

    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog())


@bot.callback_query_handler(func=lambda call: call.data.startswith('basket_item_'))
def products_call(call):
     mes = "Удалить один такой товар\n" \
     "удалить все товары этого типа\n" \
     "или вернутся назад?"
     bot.send_message(call.message.chat.id, mes, reply_markup=kb.item_choice(call.data[12:]))


# @bot.callback_query_handler(func=lambda call: call.data.startswith('choice_answer_'))
# def products_call(call):
#      if call.data.find("all"):
        

#     elif call.data.find("one"):

#     else:



@bot.callback_query_handler(func=lambda call: call.data.startswith('reg'))
def reg_phone_email(call):
    if call.data == 'reg_phone':
        msg = bot.send_message(call.message.chat.id, "введите номер телефона")
        bot.register_next_step_handler(msg, send_phone)
    
    elif call.data == "reg_email":
        msg = bot.send_message(call.message.chat.id, "введите ваш email")
        bot.register_next_step_handler(msg, send_email)
    
    bot.delete_message(call.message.chat.id, call.message.message_id)


def send_phone(message):
    users_col = ["users", "name", "phone", "email", "telegramm_id"]
    
    if db.not_occupied(users_col, "users", "phone", message.text):
        db.update_user(message.chat.id, "phone", message.text)
        bot.send_message(message.chat.id, f"Ваш номер телефона {message.text} добавлен")
    
    else:
        bot.send_message(message.chat.id, f"email {message.text} уже занят")


def send_email(message):
    users_col = ["users", "name", "phone", "email", "telegramm_id"]
    
    if db.not_occupied(users_col, "users", "email", message.text):
        db.update_user(message.chat.id, "email", message.text)
        bot.send_message(message.chat.id, f"Ваш email {message.text} добавлен")
    
    else:
        bot.send_message(message.chat.id, f"email {message.text} уже занят")



@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def pages(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    max_size = int(ceil(db.catalog_size() // 6))
    if call.data.startswith("page_+1"):
        if int(call.data[8:]) < max_size:
             bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog(int(call.data[8:]) + 1))
        
        elif int(call.data[8:]) == max_size:
            bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog())

    elif call.data.startswith("page_-1"):
        if int(call.data[8:]) == 0:
             bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog(max_size))
        
        else:
            bot.send_message(call.message.chat.id, "privet", reply_markup=kb.catalog(int(call.data[8:]) - 1))



@bot.callback_query_handler(func=lambda call: call.data.startswith('basket_page_'))
def pages(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    
    max_size = int(ceil(db.basket_size(call.message.chat.id) // 6))
    head = db.select_basket_head(call.message.chat.id)
    mes = f"Итоговая сумма: {head[3]}"
    if call.data.startswith("basket_page_+1"):
        if int(call.data[15:]) < max_size:
             bot.send_message(call.message.chat.id, mes, reply_markup=kb.basket(call.message.chat.id, int(call.data[15:]) + 1))
        
        elif int(call.data[15:]) == max_size:
            bot.send_message(call.message.chat.id, mes, reply_markup=kb.basket(call.message.chat.id))

    elif call.data.startswith("basket_page_-1"):
        if int(call.data[15:]) == 0:
             bot.send_message(call.message.chat.id, mes, reply_markup=kb.basket(call.message.chat.id, max_size))
        
        else:
           bot.send_message(call.message.chat.id, mes, reply_markup=kb.basket(call.message.chat.id, int(call.data[15:]) - 1))



@bot.callback_query_handler(func=lambda call: call.data.startswith('back'))
def answer_products_call(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if call.data == "back_products":
        head = db.select_basket_head(call.message.chat.id)
        bot.send_message(call.message.chat.id, f"Итоговая сумма: {head[3]}", reply_markup=kb.basket(call.message.chat.id))

    elif call.data == "back_basket":
        bot.send_message(call.message.chat.id, "каталог товаров:", reply_markup=kb.catalog())




@bot.message_handler(commands=['cat'])
def cat(message):
    cat = choice(['koshka', 'koshka_2', 'komury_A', 'kitten in milk',
                  'catic_mili', 'super_rjaka_demotivator_bot', 'inet', 'komury and komugi'])
    ing = open(f'cats/{cat}.mp4', 'rb')
    bot.send_animation(message.chat.id, ing, caption='test')
    ing.close()
    bot.delete_message(message.chat.id, message.message_id)




if __name__ == '__main__':
    bot.polling(none_stop=True)
