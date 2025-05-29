from aiogram import types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
import json
import os
from states import UserData

from database.database import (
    get_product_data,
    add_product_in_user_cart, 
)

from resources import (
    enter_quantity_text,
    quantity_error_text,
    creating_order_kb,
    keyboard_categories_menu,
    choise_category_text,
)
from config import CATEGORIES_NAME_FILE, IMAGES_DIR


router = Router()

    
@router.callback_query(F.data.startswith('product_id_'))
async def f_product_id(callback: types.CallbackQuery, state: FSMContext): 
    """
    Функция отображения картинки и описания выбранного товара.
    """
    await callback.message.delete()
    product_id = callback.data[11:]
    await state.update_data(product_id=product_id)
    try:
        with open(CATEGORIES_NAME_FILE, "r", encoding='utf-8') as file:
            data = json.load(file)
            category_name = data[f"{product_id[:3]}"]
            await state.update_data(category_name=category_name)
    except FileNotFoundError:
        return "Ошибка: Файл CATEGORIES_NAME_FILE не найден."
    except json.JSONDecodeError:
        return "Ошибка: Некорректный формат JSON в файле CATEGORIES_NAME_FILE."
    
    product_info = await get_product_data(category_name, product_id)
    kb = await creating_order_kb(product_info[f'{category_name}_id'])
    img = FSInputFile(os.path.join(IMAGES_DIR, F"{product_info['image_filename']}"))
    
    caption = f"""
    {product_info['description']}\n
Добавить в корзину {product_info['name']} стоимостью {product_info['price']}
    """
    
    await callback.message.answer_photo(
        photo=img,
        caption=caption,
        reply_markup=kb.as_markup(resize_keyboard=True),   
    )

    
@router.callback_query(F.data.startswith('add_to_cart_'))
async def f_add_to_cart(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция добавления товара в корзину, либо продолжение покупок.
    """
    await callback.message.delete()
    if callback.data[12:] == 'no':
        await state.clear()
        
        await callback.message.answer(
            choise_category_text,
            reply_markup=keyboard_categories_menu.as_markup(resize_keyboard=True),
        )
        
    else:      
        await callback.message.answer(
            enter_quantity_text
        )
        
        await state.set_state(UserData.product_quantity)
    

@router.message(UserData.product_quantity)
async def f_input_product_quantity(message: types.Message, state: FSMContext):  
    """
    Функция ввода количества товара.
    """
    if message.text.isdigit() == False:
        await message.answer(
            quantity_error_text
        )  
        await state.set_state(UserData.product_quantity)        
        
    else:
        await state.update_data(product_quantity=message.text)
        user_data = await state.get_data()
            
        name_table = 'user_cart' + str(message.from_user.id)
        
        await add_product_in_user_cart(
            name_table, 
            user_data['product_id'], 
            user_data['product_quantity'],
            user_data['category_name'],             
            )
        await message.answer('''Товар добавлен в корзину!''', 
                            reply_markup=keyboard_categories_menu.as_markup(resize_keyboard=True))  
      
 