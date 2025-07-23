#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_subscription_datetime_api():
    """Тестируем API подписок с DateTime полями"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API подписок с DateTime полями ===\n")
    
    # Тест 1: Получение списка подписок и проверка DateTime полей
    print("1. Получение списка подписок:")
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
                print(f"    frequency: {sub['frequency']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 2: Проверка формата DateTime в экземплярах подписок
    print("2. Проверка DateTime в экземплярах подписок:")
    try:
        response = requests.get(f"{base_url}/instances")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            for instance in data['instances'][:2]:  # Показываем первые 2
                print(f"  ID: {instance['id']}, Подписка: {instance['subscription']['name']}")
                print(f"    billing_time: {instance['billing_time']}")
                print(f"    replenishment_time: {instance['replenishment_time']}")
                print(f"    status: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Тест 3: Проверка валидации DateTime при создании экземпляра
    print("3. Проверка валидации DateTime при создании экземпляра:")
    try:
        # Получаем ID первой подписки
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            if data['subscriptions']:
                subscription_id = data['subscriptions'][0]['id']
                
                # Тестируем неверный формат даты
                invalid_instance_data = {
                    "subscription_id": subscription_id,
                    "amount": 2500,
                    "billing_time": "invalid-date",
                    "replenishment_time": "2025-07-15 10:30:00",
                    "status": "progress"
                }
                
                response = requests.post(f"{base_url}/instances", json=invalid_instance_data)
                print(f"Тест неверного формата даты - Статус: {response.status_code}")
                if response.status_code == 400:
                    print("✅ Корректно: API вернул ошибку валидации")
                else:
                    print(f"⚠️ Неожиданный статус: {response.status_code}")
            else:
                print("Нет подписок для тестирования")
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_subscription_datetime_api() 