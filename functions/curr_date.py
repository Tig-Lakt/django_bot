from datetime import datetime


async def get_current_date():
    """
    Возвращает текущую дату, для указания в файле заказов..
    """
    now = datetime.now()
    current_date = now.date()
    return current_date
