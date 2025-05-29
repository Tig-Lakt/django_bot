from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.database import (
    get_products_from_category, 
    get_more_products_from_category,
    get_faq_category,
)


########################################################################################################################
#  главное меню

btn_catalog = InlineKeyboardButton(text='🗂 Каталог', callback_data='catalog')
btn_user_cart = InlineKeyboardButton(text='🛒 Корзина', callback_data='user_cart')
btn_fag = InlineKeyboardButton(text='❓ FAQ', callback_data='faq')

head_menu_btns = [
                  btn_catalog,
                  btn_user_cart,
                  btn_fag,                  
]

keyboard_head_menu = InlineKeyboardBuilder()
keyboard_head_menu.add(*head_menu_btns)
keyboard_head_menu.adjust(1)
########################################################################################################################
#  проверка подписки

btn_check_subs = InlineKeyboardButton(text='✍🏻 Проверить подписку', callback_data='chekc_channels_subs')

check_subs = [
                  btn_check_subs,
]

keyboard_check_subs_menu = InlineKeyboardBuilder()
keyboard_check_subs_menu.add(*check_subs)
keyboard_check_subs_menu.adjust(1)

########################################################################################################################
# Кнопка возврата в главное меню

btn_back_to_main_menu = InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_main_menu')

########################################################################################################################
#  меню категорий

btn_coffee = InlineKeyboardButton(text='☕️ Кофе', callback_data='category_coffee')
btn_tea = InlineKeyboardButton(text='🍵 Чай', callback_data='category_tea')
btn_desserts = InlineKeyboardButton(text='🍰 Десерты', callback_data='category_dessert')
btn_beverages = InlineKeyboardButton(text='🧃 Напитки', callback_data='category_beverage')

categories_menu_btns = [
                  btn_coffee,
                  btn_tea,
                  btn_desserts,  
                  btn_beverages,  
                  btn_user_cart,              
]

keyboard_categories_menu = InlineKeyboardBuilder()
keyboard_categories_menu.add(*categories_menu_btns)
keyboard_categories_menu.adjust(2)


async def creating_category_kb(category) -> InlineKeyboardBuilder:
    """
    Асинхронная функция для создания встроенной клавиатуры (Inline Keyboard) с кнопками,
    для создания первой части меню с товарами.
    """
    products_data = await get_products_from_category(category)

    products_btns = []

    for item in products_data:
        btn_books = InlineKeyboardButton(text=f'{item[1]}   {item[2]}', callback_data=f'product_id_{item[0]}')
        products_btns.append(btn_books)

    btn_more = InlineKeyboardButton(text='▶️ Далее', callback_data=f'more_{category}')
    
    products_btns.append(btn_back_to_main_menu)
    products_btns.append(btn_more)
    products_kb = InlineKeyboardBuilder()
    products_kb.add(*products_btns)
    products_kb.adjust(1)

    return products_kb


async def creating_more_category_kb(category) -> InlineKeyboardBuilder:
    """
    Асинхронная функция для создания встроенной клавиатуры (Inline Keyboard) с кнопками,
    для создания второй части меню с товарами.
    """
    products_data = await get_more_products_from_category(category)

    products_btns = []

    for item in products_data:
        btn_books = InlineKeyboardButton(text=f'{item[1]}   {item[2]}', callback_data=f'product_id_{item[0]}')
        products_btns.append(btn_books)

    btn_more = InlineKeyboardButton(text='▶️ Далее', callback_data=f'more_{category}')
    
    products_btns.append(btn_back_to_main_menu)
    products_btns.append(btn_more)
    products_kb = InlineKeyboardBuilder()
    products_kb.add(*products_btns)
    products_kb.adjust(1)

    return products_kb

########################################################################################################################
#  клавиатура для оформления заказа
async def creating_order_kb(product_id) -> InlineKeyboardBuilder:
    """
    Асинхронная функция для создания встроенной клавиатуры (Inline Keyboard) с кнопками,
    для оформлеия заказа.
    """

    btn = InlineKeyboardButton(text=f'✅ Добавить в корзину', callback_data=f'add_to_cart_{product_id}')
    btn_confirmation_no = InlineKeyboardButton(text='❌ Нет', callback_data='add_to_cart_no')
    
    product_order_kb = InlineKeyboardBuilder()
    product_order_kb.add(btn, btn_confirmation_no)

    return product_order_kb

########################################################################################################################
#  клавиатура подтверждения добавления в корзину

btn_place_order = InlineKeyboardButton(text='📝 Оформить заказ', callback_data='place_order')
btn_continue_shopping = InlineKeyboardButton(text='❇️ Продолжить покупки', callback_data='back_to_main_menu')
btn_del_product = InlineKeyboardButton(text='🗑 Удалить товар', callback_data='del_product')

order_menu_btns = [
                  btn_place_order,  
                  btn_continue_shopping,  
                  btn_del_product,              
]

keyboard_order_menu = InlineKeyboardBuilder()
keyboard_order_menu.add(*order_menu_btns)
keyboard_order_menu.adjust(1)

########################################################################################################################
#  клавиатура оплаты

btn_payment = InlineKeyboardButton(text='💰 Оплатить заказ', callback_data='payment')

payment_menu_btns = [
                  btn_payment,             
]

keyboard_payment_menu = InlineKeyboardBuilder()
keyboard_payment_menu.add(*payment_menu_btns)
keyboard_payment_menu.adjust(1)
########################################################################################################################
#  клавиатура для категорий часто задаваемых вопросов
async def creating_faq_category() -> InlineKeyboardBuilder:
    """
    Асинхронная функция для создания встроенной клавиатуры (Inline Keyboard) с
    категориями FAQ.
    """

    faq_category = await get_faq_category()

    faq_category_btns = []

    for item in faq_category:
        btn_faq_category = InlineKeyboardButton(text=f"{item['category']}", callback_data=f"faq_category_{item['category']}")
        faq_category_btns.append(btn_faq_category)
    
    faq_category.append(btn_back_to_main_menu)
    faq_category_kb = InlineKeyboardBuilder()
    faq_category_kb.add(*faq_category_btns)
    faq_category_kb.adjust(2)

    return faq_category_kb

########################################################################################################################
#  клавиатура для ввода вопроса от пользователя

btn_user_ques = InlineKeyboardButton(text='Задать вопрос', callback_data='user_ques')
btn_go_head_menu = InlineKeyboardButton(text='В главное меню', callback_data='chekc_channels_subs')

user_ques_btns = [
                  btn_user_ques,   
                  btn_go_head_menu,          
]

keyboard_user_ques_menu = InlineKeyboardBuilder()
keyboard_user_ques_menu.add(*user_ques_btns)
keyboard_user_ques_menu.adjust(1)