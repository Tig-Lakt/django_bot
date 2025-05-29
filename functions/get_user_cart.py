from database.database import (
    get_product_data,
)

from resources import (
    keyboard_order_menu,
    keyboard_categories_menu,
)


async def get_user_cart(cart_data):
    """
    Возвращает пользователю содержимое корзины.
    """
    products_data = {}
    
    if cart_data is None:
        msg_text = 'Ваша корзина пуста!'
        kb = keyboard_categories_menu
        total_cost = None
        
    elif cart_data == []:
        msg_text = 'Ваша корзина пуста!'
        kb = keyboard_categories_menu
        total_cost = None
        
    elif len(cart_data) > 0:
        total_cost = 0
        for item in cart_data:
            data = await get_product_data(item['category_name'], item['product'])
            products_data[item['id']] = [data['name'], item['quantity']]
            total_cost = total_cost + (data['price'] * item['quantity'])
    
        msg_text = 'Желаете оформить заказ?\n\n'
        for key, values in products_data.items():
            msg_text = msg_text + str(key) + ' ' + values[0] + ' ---> ' + str(values[1]) + ' ' + '\n'
        
        msg_text = msg_text + '\nОбщая стоимость заказа: ' + str(total_cost)
        kb = keyboard_order_menu
    
    return msg_text, kb, total_cost