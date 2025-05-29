from aiogram import types
from aiogram.filters.command import Command
from aiogram import Router, F
from handlers.commands_handler import cmd_start
import json

from database.database import (
    get_products_from_category, 
    # count_used_vc, 
    # get_dest,
)

from resources import (
    choise_product_text,
    creating_category_kb,
    creating_more_category_kb,
)
# from config import...

from functions import (
    check_user_subs,
)


router = Router()

    
@router.callback_query(F.data.startswith('category_'))
async def f_chekc_channels_subs(callback: types.CallbackQuery): 
    await callback.message.delete()
    category = callback.data[9:]
    print(category, 'category')
    
    kb = await creating_category_kb(category)
    await callback.message.answer(
        choise_product_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
        )
    
    
@router.callback_query(F.data.startswith('more_'))
async def f_chekc_channels_subs(callback: types.CallbackQuery): 
    await callback.message.delete()
    category = callback.data[5:]
    print(category, 'more_products')
    
    kb = await creating_more_category_kb(category)
    await callback.message.answer(
        choise_product_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
        )