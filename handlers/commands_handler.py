from aiogram import types
from aiogram.filters.command import Command
from aiogram import Router, F

from resources import (
    welcome_text,
    select_action_text,
    keyboard_check_subs_menu,
    keyboard_head_menu,
)

from database.database import (
    check_user_reg, 
    registration_user,
)

from functions import (
    check_user_subs,
)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Обработчик команды `/start`.

    Приветствует пользователя и, в зависимости от того, зарегистрирован он или нет,
    добавляет его в базу данных, предлагает выбрать товар.
    """
    user_id = message.from_user.id
    try:
        user_fullname = message.from_user.full_name
    except:
        user_fullname = 'Не указано'
        
    user_reg = await check_user_reg(user_id)
    if user_reg is False:    
        await registration_user(user_id, user_fullname)
        
    user_subs = await check_user_subs(user_id)
    if user_subs is False: 
        msg_text = welcome_text
        kb = keyboard_check_subs_menu
    else:
        msg_text = select_action_text
        kb = keyboard_head_menu
        
    await message.answer(
        msg_text,
        reply_markup=kb.as_markup(resize_keyboard=True)
        )