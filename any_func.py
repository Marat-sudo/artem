import db

def checking_occurrence(list_checking, *args):
    for i in args:
        if i not in list_checking:
            return False

    return True

def all_products(page=0):
    products = db.fetc_all_products()
    one_page_products = []
    cat_size = db.catalog_size()
    for ind in range(page * 6, (page + 1) * 6):
        if ind >= cat_size:
            one_page_products.append(("cat", "пусто"))
        
        else:
            one_page_products.append(products[ind])

    return one_page_products


def all_products_from_basket(tg_id, page):
    velues = db.select_all_basket(tg_id)
    basket_list = []
    buffer_list = []
    
    size_bask = db.basket_size(tg_id)

    for product in velues:
        buffer_list.append(product[2:])

    for ind in range(page * 6, (page + 1) * 6):

        if ind >= size_bask:
            basket_list.append(("cat", "пусто"))
        
        else:
            basket_list.append(list(buffer_list[ind]))
            name = db.select_name_from_id(basket_list[-1][0])
            basket_list[-1].append(name)

    """
    ----------------------------------------------------------------------------------------------------
(1, 1, 'new', 694.5, '2025-12-15 14:43:51') [(3, 1, 217.3, 217.3), (6, 1, 57.0, 57.0), (9, 3, 105.4, 316.20000000000005), (13, 1, 104.0, 104.0), ('cat', 'пусто'), ('cat', 'пусто')]
[(3, 1, 217.3, 217.3), (6, 1, 57.0, 57.0), (9, 3, 105.4, 316.20000000000005), (13, 1, 104.0, 104.0)]
  смотри в бд
    """
    return basket_list


def sum_tuple_in_list(list_with_products):
    total_sum = 0
    for product in list_with_products:
        price, quantity = product
        total_sum = round(total_sum + price * quantity)
    
    return total_sum


def create_description(product_id):
    info = db.select_discription(product_id)
    description = f"Товар: {info[1]}\n" \
    f"количество в одной упаковке {info[2]}\n"\
    f"цена: {info[3]}\n " \
    f"количество на складе: {info[4]}" 
    return description

