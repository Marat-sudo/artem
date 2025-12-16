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


    return basket_list




def create_description(product_id):
    info = db.select_discription(product_id)
    description = f"Товар: {info[1]}\n" \
    f"количество в одной упаковке {info[2]}\n"\
    f"цена: {info[3]}\n " \
    f"количество на складе: {info[4]}" 
    return description

