from database.database import DataBase


async def create_models():
    """
    Создает таблицы в базе данных, если они еще не существуют, и заполняет таблицу packcages_wb данными.

    В случае ошибки при работе с базой данных, выводит сообщение об ошибке.
    """
    db = DataBase()
    if await db.connect():
        try:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username TEXT NOT NULL
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users_faq (
                    user_id BIGINT,
                    users_ques TEXT NOT NULL
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS coffee (
                    coffee_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INT NOT NULL,
                    image_filename TEXT
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS tea (
                    tea_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INT NOT NULL,
                    image_filename TEXT
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS dessert (
                    dessert_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INT NOT NULL,
                    image_filename TEXT
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS beverage (
                    beverage_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    price INT NOT NULL,
                    image_filename TEXT
                );''')
            
            await db.execute('''
                CREATE TABLE IF NOT EXISTS faq (
                    faq_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT,
                    category TEXT NOT NULL
                );''')
            
            await db.execute('''
                INSERT INTO coffee (coffee_id, name, description, price, image_filename) VALUES
                    ('cof_001', 'Эспрессо', 'Классический крепкий кофе', 150, 'espresso.jpg'),
                    ('cof_002', 'Американо', 'Эспрессо, разбавленный водой', 180, 'americano.jpg'),
                    ('cof_003', 'Капучино', 'Эспрессо с молочной пеной', 220, 'cappuccino.jpg'),
                    ('cof_004', 'Латте', 'Эспрессо с большим количеством молока', 250, 'latte.jpg'),
                    ('cof_005', 'Моккачино', 'Латте с шоколадом', 280, 'mocaccino.jpg'),
                    ('cof_006', 'Раф', 'Эспрессо со сливками и ванильным сахаром', 300, 'raf.jpg'),
                    ('cof_007', 'Флэт Уайт', 'Двойной эспрессо с тонким слоем молочной пены', 270, 'flat_white.jpg'),
                    ('cof_008', 'Айс Кофе', 'Холодный кофе со льдом', 200, 'ice_coffee.jpg'),
                    ('cof_009', 'Кофе по-ирландски', 'Кофе с виски и сливками', 350, 'irish_coffee.jpg'),
                    ('cof_010', 'Фильтр-кофе', 'Кофе, приготовленный методом фильтрации', 160, 'filter_coffee.jpg')
                    ON CONFLICT (coffee_id) DO NOTHING;
                ''')
            
            await db.execute('''
                INSERT INTO tea (tea_id, name, description, price, image_filename) VALUES
                    ('tea_001', 'Черный чай', 'Классический черный чай', 120, 'black_tea.jpg'),
                    ('tea_002', 'Зеленый чай', 'Бодрящий зеленый чай', 130, 'green_tea.jpg'),
                    ('tea_003', 'Белый чай', 'Нежный белый чай', 150, 'white_tea.jpg'),
                    ('tea_004', 'Улун', 'Китайский чай улун', 180, 'oolong_tea.jpg'),
                    ('tea_005', 'Ройбуш', 'Травяной чай ройбуш', 140, 'rooibos_tea.jpg'),
                    ('tea_006', 'Мятный чай', 'Чай с освежающей мятой', 150, 'mint_tea.jpg'),
                    ('tea_007', 'Фруктовый чай', 'Чай с фруктовыми добавками', 160, 'fruit_tea.jpg'),
                    ('tea_008', 'Чай с жасмином', 'Ароматный чай с жасмином', 170, 'jasmine_tea.jpg'),
                    ('tea_009', 'Имбирный чай', 'Чай с имбирем', 180, 'ginger_tea.jpg'),
                    ('tea_010', 'Чай латте', 'Чай со специями и молоком', 200, 'tea_latte.jpg')
                    ON CONFLICT (tea_id) DO NOTHING;
                ''')
            
            await db.execute('''
                INSERT INTO dessert (dessert_id, name, description, price, image_filename) VALUES
                    ('des_001', 'Шоколадный торт', 'Классический шоколадный торт', 300, 'chocolate_cake.jpg'),
                    ('des_002', 'Чизкейк', 'Нежный чизкейк', 280, 'cheesecake.jpg'),
                    ('des_003', 'Тирамису', 'Итальянский десерт тирамису', 320, 'tiramisu.jpg'),
                    ('des_004', 'Макаронс', 'Французское пирожное макаронс', 100, 'macarons.jpg'),
                    ('des_005', 'Эклер', 'Заварное пирожное эклер', 120, 'eclair.jpg'),
                    ('des_006', 'Брауни', 'Шоколадный брауни', 150, 'brownie.jpg'),
                    ('des_007', 'Круассан', 'Слоеный круассан', 80, 'croissant.jpg'),
                    ('des_008', 'Маффин', 'Английский маффин', 90, 'muffin.jpg'),
                    ('des_009', 'Печенье', 'Разнообразное печенье', 50, 'cookies.jpg'),
                    ('des_010', 'Мороженое', 'Разные вкусы мороженого', 150, 'ice_cream.jpg')
                    ON CONFLICT (dessert_id) DO NOTHING;
                ''')
            
            await db.execute('''
                INSERT INTO beverage (beverage_id, name, description, price, image_filename) VALUES
                    ('bev_001', 'Лимонад', 'Освежающий лимонад', 150, 'lemonade.jpg'),
                    ('bev_002', 'Морс', 'Ягодный морс', 160, 'mors.jpg'),
                    ('bev_003', 'Сок', 'Разные фруктовые соки', 140, 'juice.jpg'),
                    ('bev_004', 'Минеральная вода', 'Газированная и негазированная', 100, 'mineral_water.jpg'),
                    ('bev_005', 'Кока-кола', 'Классическая кола', 120, 'coca_cola.jpg'),
                    ('bev_006', 'Спрайт', 'Освежающий спрайт', 120, 'sprite.jpg'),
                    ('bev_007', 'Фанта', 'Апельсиновая фанта', 120, 'fanta.jpg'),
                    ('bev_008', 'Компот', 'Домашний компот', 130, 'compote.jpg'),
                    ('bev_009', 'Смузи', 'Фруктовый смузи', 200, 'smoothie.jpg'),
                    ('bev_010', 'Минеральная вода с лимоном', 'Минеральная вода с лимоном', 110, 'mineral_water_lemon.jpg')
                    ON CONFLICT (beverage_id) DO NOTHING;
                ''')
            
            await db.execute('''
                INSERT INTO faq (faq_id, question, answer, category) VALUES
                    ('faq_001', 'Какие способы оплаты вы принимаете?', 'Мы принимаем оплату банковскими картами (Visa, Mastercard, Maestro), электронными кошельками (например, PayPal) и наличными при самовывозе.', 'Оплата'),
                    ('faq_002', 'Как связаться с вашей службой поддержки?', 'Связаться с нашей службой поддержки можно по телефону [номер телефона] или по электронной почте [адрес электронной почты].', 'Контакты'),
                    ('faq_003', 'Можно ли изменить заказ после его оформления?', 'Изменить заказ после его оформления возможно только в течение короткого времени. Свяжитесь с нашей службой поддержки как можно скорее.', 'Заказ'),
                    ('faq_004', 'Как получить скидку на первый заказ?', 'При регистрации на нашем сайте вы автоматически получаете скидку на первый заказ.', 'Заказ'),
                    ('faq_005', 'Где найти информацию о составе товаров?', 'Информацию о составе товаров можно найти в описании товара на нашем сайте.', 'Другое')
                    ON CONFLICT (faq_id) DO NOTHING;
                ''')

        except Exception as e:
            print(f"Ошибка при работе с базой данных: {e}")

        finally:
            await db.close()