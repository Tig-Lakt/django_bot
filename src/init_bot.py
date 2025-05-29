import os
import sys

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_path)

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from handlers import (
    commands_handler,
    users_handler,
    catalog_handlers,
    product_handler,
    user_cart_handlers,
    orders_handler,
    payment_handler,
    faq_handler,
)
from models import create_models


logging.basicConfig(level=logging.INFO)


async def main():
    """
    Инициализирует и запускает Telegram-бота.

    Создает экземпляры Bot и Dispatcher, регистрирует роутеры обработчиков,
    создает таблицы в базе данных (если они не существуют) и запускает polling.
    """
    bot = Bot(token=TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(
        commands_handler.router,
        users_handler.router,
        catalog_handlers.router,
        product_handler.router,
        user_cart_handlers.router,
        orders_handler.router,
        payment_handler.router,
        faq_handler.router,
    )

    await create_models()

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
