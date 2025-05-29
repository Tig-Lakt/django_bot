from aiogram import Router, F
from aiogram import types
from resources import *
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from states import UserData

from resources import (
    select_action_text,
    keyboard_head_menu,
    successful_payment_text,
)

from database.database import (
    get_products_in_cart, 
    drop_user_cart,
)

from functions import (
    save_to_excel,
    get_current_date,
)


router = Router()
router.message.filter(F.chat.type == "private")


@router.callback_query(F.data == 'payment')
async def f_payment(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
            '''Введите сумму оплаты''', 
        ) 
    
    await state.set_state(UserData.price)


@router.message(UserData.price, ~F.successful_payment)
async def f_input_price(message: types.Message, state: FSMContext):     
    await state.update_data(price=message.text) 

    user_data = await state.get_data()
    price = user_data['price']
    
    if price.isdigit() == False:
        await message.answer(
            f'''Ошибка при вводе суммы оплаты, сумма должна быть указана цифрами. Повторите ввод.
Сумма к оплате {user_data['total_cost']}''', 
        ) 
        
        await state.set_state(UserData.price)
        
    elif int(user_data['total_cost']) != int(price):
        await message.answer(
            f'''Ошибка при вводе суммы оплаты, повторите ввод.
Сумма к оплате {user_data['total_cost']}''', 
        ) 
    
        await state.set_state(UserData.price)
    else:
        
        await state.update_data(amount=price)
        prices = [LabeledPrice(label="XTR", amount=price)]

        await message.answer_invoice(
        title='Оплата товаров',
        description=f"Сумма: {price}", 
        prices=prices,
        provider_token="",
        payload=f"{price}_stars",
        currency="XTR"
    )


@router.pre_checkout_query()
async def pre_checkout_query(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successfull_payment(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_products = await get_products_in_cart(f'user_cart{user_id}')
    
    user_data = await state.get_data()
    user_name = user_data['user_name']
    user_address = user_data['user_address']
    
    date = await get_current_date()
    
    products_data = ''
    for item in user_products:
        products_data = products_data + item['category_name'] + ' ' + item['product'] + ' ' + str(item['quantity'])
    
    data_list = [date, user_id, user_name, user_address, products_data]
    
    await save_to_excel(data_list)
    await drop_user_cart(f'user_cart{user_id}')
    await state.clear()
    await message.answer(
        successful_payment_text
    )
        
    await message.answer(
        select_action_text,
        reply_markup=keyboard_head_menu.as_markup(resize_keyboard=True)
        )