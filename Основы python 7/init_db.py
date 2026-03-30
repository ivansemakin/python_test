# init_db.py

import psycopg2
import os
from import_to_db import main_db

DB_CONFIG = {
    'dbname': 'postgres',  # Подключаемся к стандартной базе для создания новой
    'user': '1',
    'password': '1',
    'host': '127.0.0.1',
    'port': 5432
}

NEW_DB_NAME = 'farmers_markets'


def create_database():
    """Создание базы данных"""
    try:
        # Подключаемся к postgres для создания новой БД
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Проверяем существование базы
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{NEW_DB_NAME}'")
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {NEW_DB_NAME}")
                print(f"База данных {NEW_DB_NAME} создана")
            else:
                print(f"База данных {NEW_DB_NAME} уже существует")
        
        # conn.close()
        
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")
        return False
    
    return True


def execute_sql_file(sql_file_path):
    """Выполнение SQL файла"""
    try:
        # Подключаемся к новой базе
        db_config = DB_CONFIG.copy()
        db_config['dbname'] = NEW_DB_NAME
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql = f.read()

        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cur:
                # Разделяем SQL на отдельные команды
                commands = sql.split(';')
                for cmd in commands:
                    if cmd.strip():
                        cur.execute(cmd)
            conn.commit()
        
        print(f"SQL файл {sql_file_path} успешно выполнен")
        return True
        
    except Exception as e:
        print(f"Ошибка при выполнении SQL файла: {e}")
        return False


def main():
    """Инициализация базы данных"""
    print("Инициализация базы данных...")
    
    # Создаем базу данных
    if not create_database():
        return
    
    # Выполняем SQL скрипт для создания таблиц
    if os.path.exists('create_db.sql'):
        flag = execute_sql_file('create_db.sql')
        if flag:
            main_db()
    else:
        print("Файл create_db.sql не найден!")
    
    print("Инициализация завершена")


if __name__ == "__main__":
    main()