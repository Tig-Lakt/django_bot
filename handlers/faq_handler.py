from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from states import UserData

from database.database import (
    get_questions_faq_category,
    add_user_question,
)

from resources import (
    faq_text,
    user_faq_text,
    keyboard_user_ques_menu,
    successful_add_user_faq_text,
    keyboard_head_menu,
)


router = Router()

    
@router.callback_query(F.data.startswith('faq_category_'))
async def f_faq_category(callback: types.CallbackQuery, state: FSMContext): 
    """
    Функция отображения вопросов в выбранной категории FAQ.
    """
    await callback.message.delete()
    faq_category = callback.data[13:]
    
    mst_text = ''
    ques_answ = await get_questions_faq_category(faq_category)
    for item in ques_answ:
        mst_text = mst_text + f'''Вопрос: {item['question']}\n<b>Ответ: {item['answer']}</b>\n\n'''
    
    await callback.message.answer(
        mst_text
    )
    await callback.message.answer(
        faq_text,
        reply_markup=keyboard_user_ques_menu.as_markup(resize_keyboard=True)
    )
    
    
@router.callback_query(F.data == "user_ques")
async def f_user_ques(callback: types.CallbackQuery, state: FSMContext): 
    """
    Обработчик кнопки user_ques.

    Функция добавления вопроса от пользователя.
    """
    await callback.message.delete()
    
    await callback.message.answer(
        user_faq_text,
    )
    
    await state.set_state(UserData.user_faq)
    

@router.message(UserData.user_faq)
async def f_input_user_name(message: types.Message, state: FSMContext): 
    """
    Ввод текста вопроса пользователя и добавление его в базу данных.
    """
    await state.update_data(user_faq=message.text)    
    user_id = message.from_user.id
    user_data = await state.get_data()
    question_text = user_data['user_faq']
    
    await add_user_question(user_id, question_text)
    await state.clear()
    
    await message.answer(
        successful_add_user_faq_text,
        reply_markup=keyboard_head_menu.as_markup(resize_keyboard=True)
    )