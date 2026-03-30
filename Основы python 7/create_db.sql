-- create_database.sql

-- Создание базы данных (выполнить отдельно)
-- CREATE DATABASE farmers_markets
-- \c farmers_markets

-- Основная таблица рынков
CREATE TABLE IF NOT EXISTS markets (
    fmid INTEGER PRIMARY KEY,
    market_name TEXT NOT NULL,
    update_time TIMESTAMP
);

-- Таблица медиа-ссылок
CREATE TABLE IF NOT EXISTS market_media (
    fmid INTEGER PRIMARY KEY REFERENCES markets(fmid) ON DELETE CASCADE,
    website TEXT,
    facebook TEXT,
    twitter TEXT,
    youtube TEXT,
    other_media TEXT
);

-- Таблица локаций
CREATE TABLE IF NOT EXISTS market_locations (
    fmid INTEGER PRIMARY KEY REFERENCES markets(fmid) ON DELETE CASCADE,
    street TEXT,
    city TEXT,
    county TEXT,
    state TEXT,
    zip TEXT,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    location TEXT
);

-- Таблица способов оплаты
CREATE TABLE IF NOT EXISTS market_payments (
    fmid INTEGER PRIMARY KEY REFERENCES markets(fmid) ON DELETE CASCADE,
    credit BOOLEAN,
    wic BOOLEAN,
    wic_cash BOOLEAN,
    sfmnp BOOLEAN,
    snap BOOLEAN
);

-- Таблица сезонов работы
CREATE TABLE IF NOT EXISTS market_seasons (
    fmid INTEGER PRIMARY KEY REFERENCES markets(fmid) ON DELETE CASCADE,
    season1_date TEXT,
    season1_time TEXT,
    season2_date TEXT,
    season2_time TEXT,
    season3_date TEXT,
    season3_time TEXT,
    season4_date TEXT,
    season4_time TEXT
);

-- Таблица продуктов
CREATE TABLE IF NOT EXISTS market_products (
    fmid INTEGER PRIMARY KEY REFERENCES markets(fmid) ON DELETE CASCADE,
    organic BOOLEAN,
    bakedgoods BOOLEAN,
    cheese BOOLEAN,
    crafts BOOLEAN,
    flowers BOOLEAN,
    eggs BOOLEAN,
    seafood BOOLEAN,
    herbs BOOLEAN,
    vegetables BOOLEAN,
    honey BOOLEAN,
    jams BOOLEAN,
    maple BOOLEAN,
    meat BOOLEAN,
    nursery BOOLEAN,
    nuts BOOLEAN,
    plants BOOLEAN,
    poultry BOOLEAN,
    prepared BOOLEAN,
    soap BOOLEAN,
    trees BOOLEAN,
    wine BOOLEAN,
    coffee BOOLEAN,
    beans BOOLEAN,
    fruits BOOLEAN,
    grains BOOLEAN,
    juices BOOLEAN,
    mushrooms BOOLEAN,
    petfood BOOLEAN,
    tofu BOOLEAN,
    wild_harvested BOOLEAN
);

-- Таблица пользователей
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(32) NOT NULL,
    admin_rights BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица отзывов
CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL REFERENCES users(username) ON DELETE CASCADE,
    market_index INTEGER NOT NULL REFERENCES markets(fmid) ON DELETE CASCADE,
    grade INTEGER CHECK (grade >= 1 AND grade <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username, market_index)
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_markets_name ON markets(market_name);
CREATE INDEX IF NOT EXISTS idx_markets_update_time ON markets(update_time);
CREATE INDEX IF NOT EXISTS idx_locations_state_city ON market_locations(state, city);
CREATE INDEX IF NOT EXISTS idx_locations_zip ON market_locations(zip);
CREATE INDEX IF NOT EXISTS idx_reviews_market_index ON reviews(market_index);
CREATE INDEX IF NOT EXISTS idx_reviews_username ON reviews(username);