from aiogram.fsm.state import StatesGroup, State


class UserData(StatesGroup):
    """
    FSM для обработки данных пользователя.

    Состояния:
        sample (State): Ожидание ввода ....
    """
    product_id = State()
    product_quantity = State()
    category_name = State()
    del_product_id = State()
    user_name = State()
    user_address = State()
    total_cost = State()
    price = State()
    user_faq = State()