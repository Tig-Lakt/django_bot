"""
Пакет обработчиков.

Содержит модули для обработки различных типов запросов:
команд, пользовательских действий, стэйтов, регистрации и платежей.
"""

from handlers import commands_handler
from handlers import users_handler
from handlers import catalog_handlers
from handlers import product_handler 
from handlers import user_cart_handlers
from handlers import orders_handler
from handlers import payment_handler
from handlers import faq_handler