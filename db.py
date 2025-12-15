import sqlite3
import os
import any_func as fc

db_path = "data/database.db"

#def reg_phone_sql():


def user_not_reg(telegramm_id):
    conn = sqlite3.connect(db_path)    # подключаем бд
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegramm_id = ?", (telegramm_id,))  
    data = cursor.fetchone()
    return data is None

def register_user(telegramm_id, name_user):
    conn = sqlite3.connect(db_path)    # подключаем бд
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys=ON;")  
    #migrations_path = "migrations/001_create_users.sql"

    cursor.execute(
        """
        INSERT INTO users(telegramm_id, name, phone, email)
        VALUES(?, ?, ?, ?);
        """, (telegramm_id, name_user, None, None)
        )

    conn.commit()
    conn.close()


def update_user(telegramm_id, col_name, col_value):
    if col_name in ["name", "phone", "email"]:
        conn = sqlite3.connect(db_path)    # подключаем бд
        cursor = conn.cursor()
        # чтобы таблицы могли быть взаимосвязаные 
        # FOREIGN KEY (users_id) REFERENCES users(id)
        conn.execute("PRAGMA foreign_keys=ON;")
        cursor.execute(
            f"""
            UPDATE users 
            SET {col_name} = ?
            WHERE telegramm_id = ?
            """, (col_value, telegramm_id))

        conn.commit()
        conn.close()



def not_occupied(checklist, table_name, col_name, col_value):
    if fc.checking_occurrence(checklist, table_name, col_name):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            f"""SELECT {col_name}
                FROM {table_name}
                WHERE {col_name} = ? """, (col_value,)
        )

        free_values = cursor.fetchall() == []
        conn.close
    
        return free_values
  
    return False

def fetc_all_products() -> list:
    conn = sqlite3.connect(db_path)    # подключаем бд
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products ORDER BY name")
    products = cursor.fetchall()

    conn.commit()
    conn.close()
    return products

def catalog_size() -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM products")
    size = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return size

def basket_size(tg_id):
    order_id = select_order_id(select_user_id(tg_id))
    print(order_id, type(order_id))
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()

    cursor.execute("""SELECT COUNT(*) 
                   FROM order_items 
                   WHERE order_id = ?""", (order_id, ))
    size = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return size

def select_user_id(telegramm_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM users
        WHERE telegramm_id = ?
        """, (telegramm_id, )
    )
    user_id = cursor.fetchone()[0]

    conn.commit()
    conn.close()
    return user_id


def basket_is_free(user_id) -> bool:
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()
    conn.execute("PRAGMA foreign_keys=ON;")
    cursor.execute(
        """
        SELECT * FROM orders
        WHERE id = ? and (status = 'new' or status = 'pending')
        """, (user_id, )
    )
    free = cursor.fetchall() == []
    conn.commit()
    conn.close()

    return free

def create_basket(user_id) -> None:
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO orders(user_id) 
        VALUES (?)
        """, (user_id, )
    )
    conn.commit()
    conn.close()



def add_item(user_id, product_id) -> None:
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    price = select_price(product_id)
    order_id = select_order_id(user_id)
    cursor.execute(
        """
        INSERT INTO order_items(order_id, product_id, price_per_item, total_price)
        VALUES(?, ?, ?, ?)
        """, (order_id, product_id, price, 0)
    )
    conn.commit()
    conn.close()
    total_sum(order_id, product_id)
    total_sum_one_product(order_id, product_id)
    

def total_sum(order_id, product_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT total_sum FROM orders
        WHERE id = ?
        """, (order_id,))
    
    amount =  cursor.fetchone()[0]
    
    cursor.execute(
        """
        SELECT price FROM products
        WHERE id = ?
        """, (product_id,))
    
    amount = amount + cursor.fetchone()[0]
    cursor.execute(
        """
        UPDATE orders 
        SET total_sum = ?
        WHERE id = ?
        """, (amount, order_id))

    conn.commit()
    conn.close()



def total_sum_one_product(order_id, product_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT price_per_item, total_price FROM order_items
        WHERE order_id = ? and product_id = ?
        """, (order_id, product_id))
    

    total_price, price_per_item = cursor.fetchone()
    amount = total_price + price_per_item 
    cursor.execute(
        """
        UPDATE order_items
        SET total_price = ?
        WHERE product_id = ?
        """, (amount, product_id))

    conn.commit()
    conn.close()


def select_quantity(order_id, product_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT quantity FROM order_items
        WHERE order_id = ? and product_id = ?
        """, (order_id, product_id))
    
    conn.commit()
    qua_status = cursor.fetchone()
    conn.close()
    
    if qua_status is None:
        return -1
    
    return qua_status[0]


def add_quantity(quantity, order_id, product_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()
    cursor.execute(
    f"""
        UPDATE order_items 
        SET quantity = ?
        WHERE order_id = ? and product_id = ?
        """, (quantity + 1, order_id, product_id))
    
    conn.commit()
    conn.close()
    total_sum(order_id, product_id)
    total_sum_one_product(order_id, product_id)
    
    

def select_order_id(user_id):
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id FROM orders
        WHERE user_id = ? and (status = 'new' or status = 'pending')
        """, (user_id,)
    )
    id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id


def select_price(product_id) -> id:
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT price FROM products
        WHERE id = ?
        """, (product_id, )
    )

    id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return id


def user_in_db(telegramm_id):
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM users
        WHERE telegramm_id = ?
        """, (telegramm_id, )
    )

    status = not cursor.fetchall() == []
    conn.commit()
    conn.close()
    return status


def select_name_from_id(product_id):
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT name FROM products
        WHERE id = ?
        """, (product_id, )
    )

    name = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return name


def select_all_basket(telegramm_id):
    user_id = select_user_id(telegramm_id)
    order_id = select_order_id(user_id)
    conn = sqlite3.connect(db_path)   
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM orders
        WHERE user_id = ? and (status = 'new' or status = 'pending')
        """, (user_id,)
    )

    busket_head = cursor.fetchone()
    
    cursor.execute(
        """
        SELECT * FROM order_items
        WHERE order_id = ?
        """, (order_id,)
    )
    
    busket_values = cursor.fetchall()
    
    
    conn.commit()
    conn.close()
    return (busket_head, busket_values)


def select_discription(product_id):
    conn = sqlite3.connect(db_path)  
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT * FROM products
        WHERE id = ? 
        """, (product_id, )
    )

    all_info = cursor.fetchone()
    conn.close()
    return all_info

# def select_basket(order_id):
#     conn = sqlite3.connect(db_path)   
#     cursor = conn.cursor()
#     cursor.execute(
#         """
#         SELECT * FROM orders
#         WHERE id = ? and (status = 'new 'or status = 'pending')
#         """, (user_id, )
#     )

#     status = not cursor.fetchall() == []
#     conn.commit()
#     conn.close()
#     return status