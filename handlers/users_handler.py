from aiogram import types
from aiogram import Router, F

from resources import (
    not_subs_text,
    select_action_text,
    choise_category_text,
    keyboard_check_subs_menu,
    keyboard_head_menu,
    keyboard_categories_menu,
    creating_faq_category,
)

from functions import (
    check_user_subs,
)


router = Router()

    
@router.callback_query(F.data == "chekc_channels_subs")
async def f_chekc_channels_subs(callback: types.CallbackQuery): 
    """
    Функция проверки подписки на канал.
    """
    await callback.message.delete()
    user_id = callback.from_user.id
    user_subs = await check_user_subs(user_id)
    if user_subs is False: 
        msg_text = not_subs_text
        kb = keyboard_check_subs_menu
    else:
        msg_text = select_action_text
        kb = keyboard_head_menu
        
    await callback.message.answer(
        msg_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
        )
    
    
@router.callback_query(F.data == "catalog")
async def f_catalog(callback: types.CallbackQuery): 
    """
    Обработчик кнопки catalog.

    Отдает пользователю меню категорий.
    """
    await callback.message.delete()
    await callback.message.answer(
        choise_category_text,
        reply_markup=keyboard_categories_menu.as_markup(resize_keyboard=True)
        )
        
        
@router.callback_query(F.data == "faq")
async def f_catalog(callback: types.CallbackQuery): 
    """
    Обработчик кнопки catalog.

    Отдает пользователю меню категорий.
    """
    kb = await creating_faq_category()
    await callback.message.delete()
    await callback.message.answer(
        choise_category_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
        )
    
    
@router.callback_query(F.data == "back_to_main_menu")
async def f_back_to_main_menu(callback: types.CallbackQuery): 
    """
    Обработчик кнопки back_to_main_menu.

    Возвращает пользователя в главное меню.
    """
    await callback.message.delete()
    await callback.message.answer(
        choise_category_text,
        reply_markup=keyboard_categories_menu.as_markup(resize_keyboard=True)
        )