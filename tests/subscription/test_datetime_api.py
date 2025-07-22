#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_subscription_api():
    """Тестируем API подписок с новыми DateTime полями"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API подписок с DateTime полями ===\n")
    
    # Тест 1: Создание подписки с разными форматами дат
    print("1. Создание подписки с форматом 'HH:MM':")
    subscription_data = {
        "name": "Тестовая подписка",
        "amount": 1500,
        "billing_time": "15:30",
        "replenishment_time": "16:00",
        "frequency": "month",
        "source": "Банковская карта"
    }
    
    try:
        response = requests.post(base_url, json=subscription_data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"Создана подписка ID: {data['subscription']['id']}")
            print(f"billing_time: {data['subscription']['billing_time']}")
            print(f"replenishment_time: {data['subscription']['replenishment_time']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 2: Создание подписки с полным форматом даты
    print("2. Создание подписки с полным форматом даты:")
    subscription_data_full = {
        "name": "Тестовая подписка 2",
        "amount": 2000,
        "billing_time": "2025-07-22T20:00:00",
        "replenishment_time": "2025-07-22T21:00:00",
        "frequency": "year",
        "source": "Электронный кошелек"
    }
    
    try:
        response = requests.post(base_url, json=subscription_data_full)
        print(f"Статус: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"Создана подписка ID: {data['subscription']['id']}")
            print(f"billing_time: {data['subscription']['billing_time']}")
            print(f"replenishment_time: {data['subscription']['replenishment_time']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 3: Получение списка подписок
    print("3. Получение списка подписок:")
    try:
        response = requests.get(base_url)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            for sub in data['subscriptions'][:3]:  # Показываем первые 3
                print(f"  ID: {sub['id']}, {sub['name']}")
                print(f"    billing_time: {sub['billing_time']}")
                print(f"    replenishment_time: {sub['replenishment_time']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_subscription_api() 