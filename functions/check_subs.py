from config import CHANNEL_ID, TOKEN
from aiogram import Bot


bot = Bot(token=TOKEN)


async def check_user_subs(user_id):
    """
    Проверяет подписку пользователя на канал.
    """
    try:
        status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if status.status != 'left':
            return True
    except Exception as e:
        print(e)
    
    return False