# import_to_db.py

import csv
import psycopg2
from psycopg2.extras import execute_values
import os
import re
from datetime import datetime

DB_CONFIG = {
    'dbname': 'farmers_markets',
    'user': '1',
    'password': '1',
    'host': '127.0.0.1',
    'port': 5432,
    'options': '-c search_path=public'
}


def parse_csv_value(value, idx, headers):
    """Преобразование значения из CSV"""
    if value == '':
        return None
    
    if headers[idx] == 'x' or headers[idx] == 'y':
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    elif value in ('Y', 'N'):
        return value == 'Y'
    elif value == '-':
        return False
    else:
        if isinstance(value, str):
            value = value.strip()
        return value


def import_all_data(csv_file_path):
    """Импорт всех данных из CSV в базу данных"""
    
    print(f"Чтение файла {csv_file_path}...")
    
    # Чтение CSV
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        rows = []
        for row in reader:
            # if len(row) < 60:
            #     continue
            processed_row = []
            for i, value in enumerate(row):
                if i < len(headers):
                    processed_row.append(parse_csv_value(value, i, headers))
                else:
                    processed_row.append(None)
            rows.append(processed_row)
    
    print(f"Прочитано {len(rows)} записей")
    
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            
            # Очистка таблиц
            print("Очистка таблиц...")
            cur.execute("""
                TRUNCATE TABLE reviews, market_products, market_seasons, 
                market_payments, market_locations, market_media, markets 
                RESTART IDENTITY CASCADE
            """)
            
            # Импорт в markets
            print("Импорт в таблицу markets...")
            market_data = []
            for row in rows:
                if row[0] and row[1]:
                    update_time = None
                    if len(row) > 59 and row[59]:
                        try:
                            update_time = datetime.strptime(row[59], '%m/%d/%Y %H:%M:%S %p')
                        except:
                            pass
                    market_data.append((int(row[0]), row[1], update_time))
            
            execute_values(cur, """
                INSERT INTO markets (fmid, market_name, update_time)
                VALUES %s
            """, market_data)
            
            # Импорт в market_media
            print("Импорт в таблицу market_media...")
            media_data = []
            for row in rows:
                if row[0]:
                    media_data.append((
                        int(row[0]),
                        row[2] if len(row) > 2 else None,
                        row[3] if len(row) > 3 else None,
                        row[4] if len(row) > 4 else None,
                        row[5] if len(row) > 5 else None,
                        row[6] if len(row) > 6 else None
                    ))
            
            execute_values(cur, """
                INSERT INTO market_media (fmid, website, facebook, twitter, youtube, other_media)
                VALUES %s
                ON CONFLICT (fmid) DO UPDATE SET
                    website = EXCLUDED.website,
                    facebook = EXCLUDED.facebook,
                    twitter = EXCLUDED.twitter,
                    youtube = EXCLUDED.youtube,
                    other_media = EXCLUDED.other_media
            """, media_data)
            
            # Импорт в market_locations
            print("Импорт в таблицу market_locations...")
            location_data = []
            for row in rows:
                if row[0]:
                    location_data.append((
                        int(row[0]),
                        row[7] if len(row) > 7 else None,
                        row[8] if len(row) > 8 else None,
                        row[9] if len(row) > 9 else None,
                        row[10] if len(row) > 10 else None,
                        row[11] if len(row) > 11 else None,
                        row[20] if len(row) > 20 else None,
                        row[21] if len(row) > 21 else None,
                        row[22] if len(row) > 22 else None
                    ))
            
            execute_values(cur, """
                INSERT INTO market_locations (fmid, street, city, county, state, zip, x, y, location)
                VALUES %s
                ON CONFLICT (fmid) DO UPDATE SET
                    street = EXCLUDED.street,
                    city = EXCLUDED.city,
                    county = EXCLUDED.county,
                    state = EXCLUDED.state,
                    zip = EXCLUDED.zip,
                    x = EXCLUDED.x,
                    y = EXCLUDED.y,
                    location = EXCLUDED.location
            """, location_data)
            
            # Импорт в market_payments
            print("Импорт в таблицу market_payments...")
            payment_data = []
            for row in rows:
                if row[0]:
                    payment_data.append((
                        int(row[0]),
                        row[23] if len(row) > 23 else None,
                        row[24] if len(row) > 24 else None,
                        row[25] if len(row) > 25 else None,
                        row[26] if len(row) > 26 else None,
                        row[27] if len(row) > 27 else None
                    ))
            
            execute_values(cur, """
                INSERT INTO market_payments (fmid, credit, wic, wic_cash, sfmnp, snap)
                VALUES %s
                ON CONFLICT (fmid) DO UPDATE SET
                    credit = EXCLUDED.credit,
                    wic = EXCLUDED.wic,
                    wic_cash = EXCLUDED.wic_cash,
                    sfmnp = EXCLUDED.sfmnp,
                    snap = EXCLUDED.snap
            """, payment_data)
            
            # Импорт в market_seasons
            print("Импорт в таблицу market_seasons...")
            season_data = []
            for row in rows:
                if row[0]:
                    season_data.append((
                        int(row[0]),
                        row[12] if len(row) > 12 else None,
                        row[13] if len(row) > 13 else None,
                        row[14] if len(row) > 14 else None,
                        row[15] if len(row) > 15 else None,
                        row[16] if len(row) > 16 else None,
                        row[17] if len(row) > 17 else None,
                        row[18] if len(row) > 18 else None,
                        row[19] if len(row) > 19 else None
                    ))
            
            execute_values(cur, """
                INSERT INTO market_seasons (fmid, season1_date, season1_time, season2_date, season2_time, 
                    season3_date, season3_time, season4_date, season4_time)
                VALUES %s
                ON CONFLICT (fmid) DO UPDATE SET
                    season1_date = EXCLUDED.season1_date,
                    season1_time = EXCLUDED.season1_time,
                    season2_date = EXCLUDED.season2_date,
                    season2_time = EXCLUDED.season2_time,
                    season3_date = EXCLUDED.season3_date,
                    season3_time = EXCLUDED.season3_time,
                    season4_date = EXCLUDED.season4_date,
                    season4_time = EXCLUDED.season4_time
            """, season_data)
            
            # Импорт в market_products
            print("Импорт в таблицу market_products...")
            product_data = []
            for row in rows:
                if row[0]:
                    product_data.append((
                        int(row[0]),
                        row[28] if len(row) > 28 else None, row[29] if len(row) > 29 else None,
                        row[30] if len(row) > 30 else None, row[31] if len(row) > 31 else None,
                        row[32] if len(row) > 32 else None, row[33] if len(row) > 33 else None,
                        row[34] if len(row) > 34 else None, row[35] if len(row) > 35 else None,
                        row[36] if len(row) > 36 else None, row[37] if len(row) > 37 else None,
                        row[38] if len(row) > 38 else None, row[39] if len(row) > 39 else None,
                        row[40] if len(row) > 40 else None, row[41] if len(row) > 41 else None,
                        row[42] if len(row) > 42 else None, row[43] if len(row) > 43 else None,
                        row[44] if len(row) > 44 else None, row[45] if len(row) > 45 else None,
                        row[46] if len(row) > 46 else None, row[47] if len(row) > 47 else None,
                        row[48] if len(row) > 48 else None, row[49] if len(row) > 49 else None,
                        row[50] if len(row) > 50 else None, row[51] if len(row) > 51 else None,
                        row[52] if len(row) > 52 else None, row[53] if len(row) > 53 else None,
                        row[54] if len(row) > 54 else None, row[55] if len(row) > 55 else None,
                        row[56] if len(row) > 56 else None, row[57] if len(row) > 57 else None
                    ))
            
            execute_values(cur, """
                INSERT INTO market_products (fmid, organic, bakedgoods, cheese, crafts, flowers, eggs, seafood,
                    herbs, vegetables, honey, jams, maple, meat, nursery, nuts, plants, poultry, prepared,
                    soap, trees, wine, coffee, beans, fruits, grains, juices, mushrooms, petfood, tofu, wild_harvested)
                VALUES %s
                ON CONFLICT (fmid) DO UPDATE SET
                    organic = EXCLUDED.organic,
                    bakedgoods = EXCLUDED.bakedgoods,
                    cheese = EXCLUDED.cheese,
                    crafts = EXCLUDED.crafts,
                    flowers = EXCLUDED.flowers,
                    eggs = EXCLUDED.eggs,
                    seafood = EXCLUDED.seafood,
                    herbs = EXCLUDED.herbs,
                    vegetables = EXCLUDED.vegetables,
                    honey = EXCLUDED.honey,
                    jams = EXCLUDED.jams,
                    maple = EXCLUDED.maple,
                    meat = EXCLUDED.meat,
                    nursery = EXCLUDED.nursery,
                    nuts = EXCLUDED.nuts,
                    plants = EXCLUDED.plants,
                    poultry = EXCLUDED.poultry,
                    prepared = EXCLUDED.prepared,
                    soap = EXCLUDED.soap,
                    trees = EXCLUDED.trees,
                    wine = EXCLUDED.wine,
                    coffee = EXCLUDED.coffee,
                    beans = EXCLUDED.beans,
                    fruits = EXCLUDED.fruits,
                    grains = EXCLUDED.grains,
                    juices = EXCLUDED.juices,
                    mushrooms = EXCLUDED.mushrooms,
                    petfood = EXCLUDED.petfood,
                    tofu = EXCLUDED.tofu,
                    wild_harvested = EXCLUDED.wild_harvested
            """, product_data)
            
            conn.commit()
            print("Импорт успешно завершен!")


def main_db():
    csv_file = 'Export.csv'
    
    if not os.path.exists(csv_file):
        print(f"Ошибка: файл {csv_file} не найден!")
        return
    
    try:
        import_all_data(csv_file)
        
        # Выводим статистику
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM markets")
                markets_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM users")
                users_count = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM reviews")
                reviews_count = cur.fetchone()[0]
                
                print(f"\nСтатистика базы данных:")
                print(f"  Рынков: {markets_count}")
                print(f"  Пользователей: {users_count}")
                print(f"  Отзывов: {reviews_count}")
                
    except Exception as e:
        print(f"Ошибка при импорте: {e}")


if __name__ == "__main__":
    main_db()
    