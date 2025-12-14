from config import TOKEN
import db
import telebot
bot = telebot.TeleBot(TOKEN)


def _basket_func(user_id, product_id):
        order_id = db.select_order_id(user_id)
        quantity_items = db.select_quantity(order_id, product_id)

        if quantity_items == -1:
            db.add_item(user_id, product_id)
            
        else:
            db.add_quantity(quantity_items, order_id, product_id)
            
        

def basket(user_id, product_id):
    if db.basket_is_free(user_id):
        db.create_basket(user_id)
        _basket_func(user_id, product_id)
        
    else:
        _basket_func(user_id, product_id)

    