CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pickup_location VARCHAR(100),  -- Откуда
    dropoff_location VARCHAR(100), -- Куда
    distance_km DECIMAL(5, 2),     -- Расстояние
    fare_amount DECIMAL(10, 2),    -- Цена
    rating INTEGER,                -- Рейтинг (1-5)
    service_type VARCHAR(20)       -- Тип: 'Такси', 'Доставка'
);