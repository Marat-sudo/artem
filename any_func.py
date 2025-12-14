import db

def checking_occurrence(list_checking, *args):
    for i in args:
        if i not in list_checking:
            return False

    return True

def all_products(page=0):
    products = db.fetc_all_products()
    one_page_products = []
    for ind in range(page * 6, (page + 1) * 6):
        if ind >= db.catalog_size():
            one_page_products.append(("cat", "пусто"))
        
        else:
            one_page_products.append(products[ind])

    return one_page_products


def sum_tuple_in_list(list_with_products):
    total_sum = 0
    for product in list_with_products:
        print(product)
        price, quantity = product
        total_sum = total_sum + price * quantity
    
    return total_sum