"""
Пакет config.

Содержит константы и настройки, необходимые для работы бота.

Экспортируемые переменные:
    TOKEN (str): Токен Telegram-бота.
    PROJECT_PATH (str): Путь к корневой директории проекта.
    DB_CONN (list): Данные для подключения к БД.
    CHANNEL_ID (int): ID канала, в котором бот проверяет подписку.
    CATEGORIES_NAME_FILE (str): Путь к файлу с категориями.
    IMAGES_DIR (str): Путь к директории, в которой хранятся изображения товаров.
    XLSX_NAME_FILE (str): Путь к файлу с заказами.
"""

from config.constants import TOKEN
from config.constants import PROJECT_PATH
from config.constants import DB_CONN
from config.constants import CHANNEL_ID
from config.constants import CATEGORIES_NAME_FILE
from config.constants import IMAGES_DIR
from config.constants import XLSX_NAME_FILE
