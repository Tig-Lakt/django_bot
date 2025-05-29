
"""
Модуль database.py

Обеспечивает асинхронное взаимодействие с базой данных PostgreSQL
с использованием библиотеки asyncpg.  Параметры подключения загружаются
из переменных окружения.
"""

import asyncpg
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from config import DB_CONN


class DataBase:
    """
    Класс для управления подключением к базе данных PostgreSQL и выполнения запросов.
    Параметры подключения загружаются из переменных окружения.
    """
    print(DB_CONN)
    def __init__(self):
        """
        Инициализирует объект DataBase с параметрами подключения из переменных окружения.

        Переменные окружения:
            DB_HOST (str): Хост базы данных.
            DB_PORT (str): Порт базы данных.
            DB_NAME (str): Имя базы данных.
            DB_USER (str): Имя пользователя базы данных.
            DB_PASSWORD (str): Пароль пользователя базы данных.

        Raises:
            ValueError: Если какая-либо из необходимых переменных окружения не установлена.
        """
        self.host = DB_CONN[0]
        self.port = DB_CONN[1]
        self.database = DB_CONN[2]
        self.user = DB_CONN[3]
        self.password = DB_CONN[4]

        if not all([self.host, self.port, self.database, self.user, self.password]):
            raise ValueError(
                "Необходимо установить переменные окружения: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
            )

        self.connection = None
        self.dsn = (
            f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

    async def connect(self) -> bool:
        """
        Устанавливает асинхронное подключение к базе данных.

        Returns:
            bool: True, если подключение успешно установлено, False - в противном случае.
        """
        try:
            self.connection = await asyncpg.connect(self.dsn)
            logger.info("Успешно подключено к PostgreSQL!")
            return True
        except asyncpg.PostgresConnectionError as e:
            logger.error(f"Ошибка подключения к PostgreSQL: {e}")
            return False

    async def execute(self, query: str, *args) -> bool:
        """
        Выполняет асинхронный запрос к базе данных без возврата данных.

        Используется для выполнения операций INSERT, UPDATE, DELETE и CREATE.

        Args:
            query (str): SQL-запрос для выполнения.
            *args: Аргументы для подстановки в запрос.

        Returns:
            bool: True, если запрос успешно выполнен, False - в противном случае.
        """
        if self.connection is None:
            logger.error("Ошибка: Нет активного подключения к базе данных.")
            return False

        try:
            await self.connection.execute(query, *args)
            return True
        except Exception as e:
            logger.exception(f"Ошибка выполнения запроса: {e}")  # Log the exception
            return False

    async def fetch(self, query: str, *args) -> list[asyncpg.Record] | None:
        """
        Выполняет асинхронный запрос SELECT и возвращает результаты в виде списка.

        Args:
            query (str): SQL-запрос для выполнения.
            *args: Аргументы для подстановки в запрос.

        Returns:
            list[asyncpg.Record] | None: Список строк (asyncpg.Record),
            если запрос успешно выполнен, None - в случае ошибки или отсутствия подключения.
        """
        if self.connection is None:
            logger.error("Ошибка: Нет активного подключения к базе данных.")
            return None

        try:
            rows = await self.connection.fetch(query, *args)
            return rows
        except Exception as e:
            logger.exception(f"Ошибка выполнения запроса: {e}")  # Log the exception
            return None

    async def fetchrow(self, query: str, *args) -> asyncpg.Record | None:
        """
        Выполняет асинхронный запрос SELECT и возвращает одну строку.

        Args:
            query (str): SQL-запрос для выполнения.
            *args: Аргументы для подстановки в запрос.

        Returns:
            asyncpg.Record | None: Объект asyncpg.Record, представляющий строку,
            если запрос успешно выполнен, None - в случае ошибки или отсутствия подключения.
        """
        if self.connection is None:
            logger.error("Ошибка: Нет активного подключения к базе данных.")
            return None

        try:
            row = await self.connection.fetchrow(query, *args)
            return row
        except Exception as e:
            logger.exception(f"Ошибка выполнения запроса: {e}")  # Log the exception
            return None

    async def close(self):
        """
        Закрывает асинхронное соединение с базой данных.
        """
        if self.connection:
            await self.connection.close()
            logger.info("Соединение с PostgreSQL закрыто.")
        else:
            logger.warning("Нет активного соединения для закрытия.")


async def check_user_reg(user_id) -> list[asyncpg.Record] | None:
    """
    Проверяет подписку пользователя. Возвращает True, если пользователь есть 
    в базе данных, False, если еще нет.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        user_reg = await db.fetch(f"""SELECT user_id 
                                        FROM users
                                        WHERE user_id = {user_id};""")
        
        if user_reg == []:
            return False
        return True

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def registration_user(user_id, username):
    """
    Регистрирует пользователя в базе данных.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None
        
        await db.execute(f"""INSERT INTO users (user_id, username) VALUES
                                ({user_id}, '{username}');""")
        

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
       
async def get_products_from_category(category) -> list[asyncpg.Record] | None:
    """
    Возвращает список список товаров для первой части меню категории.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        products = await db.fetch(f"""SELECT {category}_id, name, price
                                  FROM {category}
                                  ORDER BY {category}_id 
                                  LIMIT 5;""")
        return products

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def get_more_products_from_category(category) -> list[asyncpg.Record] | None:
    """
    Возвращает список список товаров для второй части меню категории.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        products = await db.fetch(f"""SELECT {category}_id, name, price
                                  FROM {category}
                                  ORDER BY {category}_id DESC
                                  LIMIT 5;""")
        return products

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def add_product_in_user_cart(name_table, product_id, quantity, category_name):
    """
    Создает таблицу для козины пользователя, если ее еще нет, добавляет товары в корзину.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        await db.execute(f"""CREATE TABLE IF NOT EXISTS {name_table}
                                (id SERIAL,
                                product TEXT NOT NULL,
                                quantity INT NOT NULL,
                                category_name TEXT NOT NULL);""")
        
        await db.execute(f"""INSERT INTO {name_table} (product, quantity, category_name) VALUES
                                ('{product_id}', {quantity}, '{category_name}');""")
        

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
        
async def get_product_data(category_name, product_id) -> list[asyncpg.Record] | None:
    """
    Возвращает характеристики указанного товара
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        product_data = await db.fetchrow(f"""SELECT *
                                  FROM {category_name}
                                  WHERE {category_name}_id = '{product_id}';""")
        return product_data

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def get_products_in_cart(user_cart) -> list[asyncpg.Record] | None:
    """
    Возвращает список всех товаров из корзины пользователя.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        cart_data = await db.fetch(f"""SELECT *
                                  FROM {user_cart};""")
        return cart_data

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()


async def del_product_in_user_cart(name_table, del_product_id):
    """
    Удаляет товар из корзины пользователя.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None
        
        await db.execute(f"""DELETE FROM {name_table}
                             WHERE id = {del_product_id};""")

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()


async def drop_user_cart(name_table, ):
    """
    Удаляет таблицу "корзина пользователя".
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None
        
        await db.execute(f"""DROP TABLE {name_table};""")

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def get_faq_category() -> list[asyncpg.Record] | None:
    """
    Возвращает список категорий для часто задаваемых вопросов..
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        faq_category = await db.fetch(f"""SELECT DISTINCT category FROM faq;""")
        
        return faq_category

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def get_questions_faq_category(category) -> list[asyncpg.Record] | None:
    """
    Возвращает список вопросов в выбранной категории часто задаваемых вопросов..
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None

        questions_category = await db.fetch(f"""SELECT question, answer
                                                FROM faq
                                                WHERE category = '{category}' 
                                                ;""")
        
        return questions_category

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()
            
            
async def add_user_question(user_id, question_text):
    """
    Создает таблицу для козины пользователя, если ее еще нет, добавляет товары в корзину.
    """
    db = DataBase()
    try:
        if not await db.connect():
            logger.error("Не удалось подключиться к базе данных.")
            return None
        
        await db.execute(f"""INSERT INTO users_faq (user_id, users_ques) VALUES
                                ({user_id}, '{question_text}');""")
        

    except Exception as e:
        logger.exception(f"Ошибка при работе с базой данных: {e}")
        return None
    finally:
        if db.connection:
            await db.close()