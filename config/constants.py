"""
Модуль config.constants

Содержит константы и настройки, используемые в проекте, такие как токен бота,
пути к файлам с данными и др.
"""

import os
import sys
from utils import get_bot_token, get_db_connection_params, update_config_file


update_config_file()

# Получаем абсолютный путь к корневой директории проекта.
# Используем os.path.dirname(__file__) для получения пути к текущему файлу (constants.py),
# затем переходим на один уровень выше, чтобы получить путь к PROJECT_PATH.
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Добавляем путь к проекту в sys.path, чтобы можно было импортировать модули из проекта.
sys.path.insert(0, PROJECT_PATH)

# Получаем токен бота из переменной окружения или файла конфигурации (см. utils.py).
TOKEN = get_bot_token()

# Получаем данные подключения к базе данных из переменной окружения или файла конфигурации (см. utils.py).
DB_CONN = get_db_connection_params()

CHANNEL_ID = '-1002319927231'


# Пути к файлам с данными.
# Используем os.path.join() для построения путей, что обеспечивает
# кросс-платформенную совместимость.
JSON_DIR = os.path.join(PROJECT_PATH, "data", "json") # Создаем переменную для пути к директории с данными
CATEGORIES_NAME_FILE = os.path.join(JSON_DIR, "categories_name.json")

IMAGES_DIR = os.path.join(PROJECT_PATH, "data", "images") # Создаем переменную для пути к директории с данными
XLSX_DIR = os.path.join(PROJECT_PATH, "data", "xlsx")
XLSX_NAME_FILE = os.path.join(XLSX_DIR, "orders.xlsx")