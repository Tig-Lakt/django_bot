from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import UserData

from database.database import (
    get_products_in_cart, 
)

from resources import (
    user_name_text,
    keyboard_payment_menu,
)

from functions import (
    get_user_cart,
)


router = Router()


@router.callback_query(F.data == "place_order")
async def f_place_order(callback: types.CallbackQuery, state: FSMContext): 
    """
    Обработчик кнопки place_order.

    Функция оформление заказа.
    """
    await callback.message.delete()
    user_id = callback.from_user.id  
    cart_data = await get_products_in_cart(f'user_cart{user_id}')
    data = await get_user_cart(cart_data)
    
    await state.update_data(total_cost=data[2]) 
    msg_text = data[0] + '\n\n' + 'Введите адрес доставки'
    
    await callback.message.answer(
            msg_text, 
        ) 
    
    await state.set_state(UserData.user_address)
    
    
@router.message(UserData.user_address)
async def f_input_user_address(message: types.Message, state: FSMContext): 
    """
    Ввод адреса доставки.
    """
    await state.update_data(user_address=message.text) 
    await message.answer(
            user_name_text, 
        ) 
    
    await state.set_state(UserData.user_name)
    
    
@router.message(UserData.user_name)
async def f_input_user_name(message: types.Message, state: FSMContext): 
    """
    Ввод имени заказчика.
    """
    await state.update_data(user_name=message.text)    
    
    user_data = await state.get_data()
    total_cost = user_data['total_cost']
    
    await message.answer(
            f'''Заказ успешно сформирован. Пожалуйста, оплатите Ваши покупки.
Сумма к оплате {total_cost}''',
            reply_markup=keyboard_payment_menu.as_markup(resize_keyboard=True), 
        ) 
    
    