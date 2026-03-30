# db_util.py

import psycopg2
from psycopg2.extras import execute_values
import hashlib
import math
from datetime import datetime

# Конфигурация базы данных
DB_CONFIG = {
    'dbname': 'farmers_markets',
    'user': '1',
    'password': '1',
    'host': '127.0.0.1',
    'port': 5432
    # 'options': '-c search_path=public'
}

# Глобальные переменные для кэширования данных
_markets_cache = None
_markets_timestamp = None


def get_db_connection():
    """Получение соединения с базой данных"""
    return psycopg2.connect(**DB_CONFIG)


def read_market_all():
    """
    Чтение всех данных о рынках из базы данных
    Возвращает список всех рынков в том же формате, что и исходный CSV
    """
    global _markets_cache, _markets_timestamp
    
    # Кэширование данных на 5 минут
    if _markets_cache is not None and _markets_timestamp is not None:
        if (datetime.now() - _markets_timestamp).seconds < 300:
            return _markets_cache
    
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Получаем все данные из связанных таблиц
            cur.execute("""
                SELECT 
                    m.fmid, m.market_name,
                    med.website, med.facebook, med.twitter, med.youtube, med.other_media,
                    loc.street, loc.city, loc.county, loc.state, loc.zip,
                    s.season1_date, s.season1_time, s.season2_date, s.season2_time,
                    s.season3_date, s.season3_time, s.season4_date, s.season4_time,
                    loc.x, loc.y, loc.location,
                    pay.credit, pay.wic, pay.wic_cash, pay.sfmnp, pay.snap,
                    prod.organic, prod.bakedgoods, prod.cheese, prod.crafts, prod.flowers,
                    prod.eggs, prod.seafood, prod.herbs, prod.vegetables, prod.honey,
                    prod.jams, prod.maple, prod.meat, prod.nursery, prod.nuts,
                    prod.plants, prod.poultry, prod.prepared, prod.soap, prod.trees,
                    prod.wine, prod.coffee, prod.beans, prod.fruits, prod.grains,
                    prod.juices, prod.mushrooms, prod.petfood, prod.tofu, prod.wild_harvested,
                    m.update_time
                FROM markets m
                LEFT JOIN market_media med ON m.fmid = med.fmid
                LEFT JOIN market_locations loc ON m.fmid = loc.fmid
                LEFT JOIN market_payments pay ON m.fmid = pay.fmid
                LEFT JOIN market_seasons s ON m.fmid = s.fmid
                LEFT JOIN market_products prod ON m.fmid = prod.fmid
                ORDER BY m.fmid
            """)
            
            rows = cur.fetchall()
            
            # Преобразуем в формат, совместимый с существующим кодом
            all_info = []
            for row in rows:
                market_row = list(row)
                # Преобразуем булевы значения обратно в Y/N для совместимости
                for i in range(23, 58):
                    if market_row[i] is True:
                        market_row[i] = 'Y'
                    elif market_row[i] is False:
                        market_row[i] = 'N'
                    elif market_row[i] is None:
                        market_row[i] = ''
                all_info.append(market_row)
            
            _markets_cache = all_info
            _markets_timestamp = datetime.now()
            return all_info


def decomposition(codes):
    """
    Декомпозиция данных о рынках на отдельные категории
    """
    FMID_codes = []
    media_codes = []
    location_codes = []
    payment_codes = []
    season_codes = []
    products_codes = []
    
    for line in range(len(codes)):
        FMID_codes.append(codes[line][0:2])
        FMID_codes[line].append(codes[line][59] if len(codes[line]) > 59 else '')
        media_codes.append(codes[line][2:7])
        location_codes.append(codes[line][7:12])
        location_codes[line].extend(codes[line][20:23])
        payment_codes.append(codes[line][23:28])
        season_codes.append(codes[line][12:20])
        products_codes.append(codes[line][28:58])
    
    return FMID_codes, media_codes, location_codes, payment_codes, season_codes, products_codes


def add_user_to_db(username, password, is_admin=False):
    """
    Добавление пользователя в базу данных
    """
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (username, password_hash, admin_rights)
                    VALUES (%s, %s, %s)
                """, (username, hashed_password, is_admin))
                conn.commit()
                return True
    except psycopg2.IntegrityError:
        return False
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False


def authenticate_user(username, password):
    """
    Аутентификация пользователя
    Возвращает (success, is_admin, error_code)
    """
    input_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, password_hash, admin_rights 
                    FROM users 
                    WHERE username = %s
                """, (username,))
                
                row = cur.fetchone()
                
                if row is None:
                    return False, False, 3  # Пользователь не найден
                
                if row[1] == input_hash:
                    return True, row[2], 0  # Успешная аутентификация
                else:
                    return False, False, 2  # Неверный пароль
                    
    except Exception as e:
        print(f"Ошибка при аутентификации: {e}")
        return False, False, 1  # Ошибка подключения


def save_market_review(username, market_index, grade, review=""):
    """
    Сохранение или обновление отзыва о рынке
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Проверяем существование отзыва
                cur.execute("""
                        SELECT 1 FROM reviews 
                        WHERE username = %s AND market_index = %s
                    """, (username, market_index))

                if cur.fetchone():
                    # Обновляем существующий отзыв
                    cur.execute("""
                            UPDATE reviews 
                            SET grade = %s, review = %s, updated_at = CURRENT_TIMESTAMP
                            WHERE username = %s AND market_index = %s
                        """, (grade, review, username, market_index))
                else:
                    # Создаем новый отзыв
                    cur.execute("""
                            INSERT INTO reviews (username, market_index, grade, review, created_at, updated_at)
                            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """, (username, market_index, grade, review))

                conn.commit()
                return True
    except Exception as e:
        print(f"Ошибка при сохранении отзыва: {e}")
        return False


def find_review_on_market(market_index):
    """
    Поиск всех отзывов о конкретном рынке
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, market_index, grade, review, created_at, id
                    FROM reviews
                    WHERE market_index = %s
                    ORDER BY created_at DESC
                """, (market_index,))
                results = cur.fetchall()
                return results if results else []
    except Exception as e:
        print(f"Ошибка при поиске отзывов: {e}")
        return []


def get_market_grade(market_index):
    """
    Получение средней оценки рынка
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG(grade) as avg_grade
                    FROM reviews
                    WHERE market_index = %s
                """, (market_index,))
                result = cur.fetchone()
                return result[0] if result and result[0] is not None else None
    except Exception as e:
        print(f"Ошибка при получении оценки: {e}")
        return None


def delete_market_review(username, review_id, is_admin):
    """
    Удаление отзыва о рынке
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                if is_admin:
                    cur.execute("""
                                        DELETE FROM reviews
                                        WHERE id = %s
                                    """, str(review_id))
                else:
                    cur.execute("""
                        DELETE FROM reviews
                        WHERE username = %s AND id = %s
                    """, (username, str(review_id)))
                conn.commit()
                return cur.rowcount > 0
    except Exception as e:
        print(f"Ошибка при удалении отзыва: {e}")
        return False


def read_all_reviews():
    """
    Чтение всех отзывов из базы данных
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT username, market_index, grade, review, created_at
                    FROM reviews
                    ORDER BY created_at DESC
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Ошибка при чтении отзывов: {e}")
        return []


def find_markets_by_location(city, state, zip_code, max_miles=10):
    """
    Поиск рынков по местоположению в радиусе max_miles миль
    """
    # Сначала находим координаты целевого рынка
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT x, y FROM market_locations
                WHERE city = %s AND state = %s AND zip = %s
                AND x IS NOT NULL AND y IS NOT NULL
            """, (city, state, zip_code))
            
            target = cur.fetchone()
            if not target:
                return []
            
            target_lat, target_lon = target
            
            # Получаем все рынки с координатами
            cur.execute("""
                SELECT m.fmid, m.market_name, loc.x, loc.y, loc.city, loc.state, loc.zip
                FROM markets m
                JOIN market_locations loc ON m.fmid = loc.fmid
                WHERE loc.x IS NOT NULL AND loc.y IS NOT NULL
            """)
            
            markets = cur.fetchall()
            result = []

            counter = 0
            for market in markets:
                fmid, name, lat, lon, city_name, state_name, zip_val = market
                if lat is not None and lon is not None:
                    distance = distance_to_another_point(target_lat, lat, target_lon, lon)
                    if distance <= max_miles:
                        # result.append([fmid, name, distance, city_name, state_name, zip_val])
                        result.append([counter,distance])
                counter+=1

            
            # Сортируем по расстоянию
            # result.sort(key=lambda x: x[2])
            return result


def distance_to_another_point(lat1, lat2, lon1, lon2):
    """Вычисление расстояния между двумя точками в милях"""
    R_earth_miles = 3958.75
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon1 - lon2)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    central_angle = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R_earth_miles * central_angle


def get_market_by_id(fmid):
    """
    Получение полной информации о рынке по ID
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    m.fmid, m.market_name,
                    med.website, med.facebook, med.twitter, med.youtube, med.other_media,
                    loc.street, loc.city, loc.county, loc.state, loc.zip,
                    s.season1_date, s.season1_time, s.season2_date, s.season2_time,
                    s.season3_date, s.season3_time, s.season4_date, s.season4_time,
                    loc.x, loc.y, loc.location,
                    pay.credit, pay.wic, pay.wic_cash, pay.sfmnp, pay.snap,
                    prod.organic, prod.bakedgoods, prod.cheese, prod.crafts, prod.flowers,
                    prod.eggs, prod.seafood, prod.herbs, prod.vegetables, prod.honey,
                    prod.jams, prod.maple, prod.meat, prod.nursery, prod.nuts,
                    prod.plants, prod.poultry, prod.prepared, prod.soap, prod.trees,
                    prod.wine, prod.coffee, prod.beans, prod.fruits, prod.grains,
                    prod.juices, prod.mushrooms, prod.petfood, prod.tofu, prod.wild_harvested,
                    m.update_time
                FROM markets m
                LEFT JOIN market_media med ON m.fmid = med.fmid
                LEFT JOIN market_locations loc ON m.fmid = loc.fmid
                LEFT JOIN market_payments pay ON m.fmid = pay.fmid
                LEFT JOIN market_seasons s ON m.fmid = s.fmid
                LEFT JOIN market_products prod ON m.fmid = prod.fmid
                WHERE m.fmid = %s
            """, (fmid,))
            
            row = cur.fetchone()
            if row:
                market_row = list(row)
                # Преобразуем булевы значения
                for i in range(23, 58):
                    if market_row[i] is True:
                        market_row[i] = 'Y'
                    elif market_row[i] is False:
                        market_row[i] = 'N'
                    elif market_row[i] is None:
                        market_row[i] = ''
                return market_row
            return None


def get_market_count():
    """Получение общего количества рынков"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM markets")
            return cur.fetchone()[0]


def get_markets_paginated(offset, limit):
    """
    Получение списка рынков с пагинацией
    """
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT fmid, market_name FROM markets
                ORDER BY fmid
                LIMIT %s OFFSET %s
            """, (limit, offset))
            return cur.fetchall()


def get_markets_sorted_by(sort_by, order='ASC'):
    """
    Получение отсортированного списка рынков
    sort_by: 'city', 'state', 'zip'
    order: 'ASC' или 'DESC'
    """
    sort_mapping = {
        'city': 'loc.city',
        'state': 'loc.state',
        'zip': 'loc.zip'
    }

    if sort_by not in sort_mapping:
        return get_markets_paginated(0, 10000)

    sort_column = sort_mapping[sort_by]
    order_direction = 'ASC' if order == 'ASC' else 'DESC'

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT m.fmid, m.market_name
                    FROM markets m
                    LEFT JOIN market_locations loc ON m.fmid = loc.fmid
                    ORDER BY {sort_column} {order_direction}, m.fmid
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"Ошибка при сортировке: {e}")
        return []
