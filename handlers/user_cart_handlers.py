from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import UserData

from database.database import (
    get_products_in_cart, 
    del_product_in_user_cart,
)

from resources import (
    del_product_from_cart_text,
    del_product_from_cart_error_text,
    del_product_text,
    keyboard_order_menu,
)

from functions import (
    get_user_cart,
)


router = Router()


@router.callback_query(F.data == "user_cart")
async def f_user_cart(callback: types.CallbackQuery): 
    """
    Обработчик кнопки user_cart.

    Отдает пользователю содержимое корзины.
    """
    await callback.message.delete()
    user_id = callback.from_user.id  
    cart_data = await get_products_in_cart(f'user_cart{user_id}')
    data = await get_user_cart(cart_data)
    
    await callback.message.answer(
            data[0], 
            reply_markup=data[1].as_markup(resize_keyboard=True)
        )
        

@router.callback_query(F.data == "del_product")
async def f_del_product(callback: types.CallbackQuery, state: FSMContext): 
    """
    Обработчик кнопки del_product.

    Функция удаления выбранного товара из корзины.
    """
    await callback.message.answer(
            del_product_from_cart_text
        )
    
    await state.set_state(UserData.del_product_id)
    

@router.message(UserData.del_product_id)
async def f_input_del_product_id(message: types.Message, state: FSMContext):
    """
    Ввод ID товара для удаления и удаление его из корзины.
    """  
    if message.text.isdigit() == False:
        await message.answer(
            del_product_from_cart_error_text
        ) 
        await state.set_state(UserData.del_product_id)        
        
    else:
        user_id = message.from_user.id
        await state.update_data(del_product_id=message.text)
        user_data = await state.get_data()
        await del_product_in_user_cart(f'user_cart{user_id}', user_data['del_product_id'])
        
        await message.answer(
            del_product_text,
            reply_markup=keyboard_order_menu.as_markup(resize_keyboard=True)
            
        )