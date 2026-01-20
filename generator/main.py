import time
import psycopg2
import random
import re
import sys


def load_streets():
    """
    Загружает улицы из текстового файла  
    Возвращает: list: список из name, max и type
    """
    categorized_data = []
    try:
        with open('streets.txt', 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
        
        # Определяем тип
        for index, line in enumerate(lines):
            if index < 12:
                st_type = "пер."
            elif 12 <= index < 19: # 12 + 7 = 19
                st_type = "пр-кт"
            else:
                st_type = "ул."
            
            match = re.search(r'(\d+)\s+дом', line)
            if match:
                max_houses = int(match.group(1))
                name = line[:match.start()].strip()
                
                categorized_data.append({
                    "name": name,
                    "max": max_houses,
                    "type": st_type
                })
        return categorized_data
    
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}", flush=True)
        return []

MY_STREETS = load_streets()

def get_random_address():
    """
    Выбирает случайную улицу из MY_STREETS и возвращает адрес с номером дома.
    Возвращает: str: Полная строка адреса в формате "тип название, д. номер".
    """
    if not MY_STREETS:
        return "ул. Неизвестная, д. 1"
    
    selection = random.choice(MY_STREETS)
    house_num = random.randint(1, selection["max"]) # Учитываем кол-во домов на улице
    
    return f"{selection['type']} {selection['name']}, д. {house_num}"

print("Генератор запущен, подключаемся к базе...", flush=True)

while True:
    try:
        conn = psycopg2.connect(
            dbname="taxi_db", 
            user="Tsuki", 
            password="545610", 
            host="db"
        )
        break
    except psycopg2.OperationalError:
        print("База данных еще не готова... Ждем 2 секунды", flush=True)
        time.sleep(4)

cursor = conn.cursor()

print("Успешное подключение! Начинаем генерацию...", flush=True)

while True:
    try:
        pickup = get_random_address()
        dropoff = get_random_address()
        
        while pickup == dropoff:
            dropoff = get_random_address()
        
        distance = round(random.uniform(1.5, 20.0), 2)

        if distance > 15.0:
            pop = [1, 2, 3, 4, 5]
            wts = [0.15, 0.15, 0.20, 0.20, 0.30]
        else:
            pop = [1, 2, 3, 4, 5]
            wts = [0.02, 0.03, 0.10, 0.25, 0.60]

        fare = round(distance * 12.5, 2)
        rating = random.choices(pop, weights=wts)[0]
        s_type = random.choice(['Такси', 'Доставка'])

        # Запись в базу
        cursor.execute("""
            INSERT INTO trips (pickup_location, dropoff_location, distance_km, fare_amount, rating, service_type) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (pickup, dropoff, distance, fare, rating, s_type))
        
        conn.commit()
        print(f"[{s_type.upper()}] {pickup} -> {dropoff} | {distance} км. | {fare} руб. | {rating} |", flush=True)
        
        time.sleep(1)
        
    except Exception as e:
        print(f"Ошибка в цикле: {e}", flush=True)
        time.sleep(5)