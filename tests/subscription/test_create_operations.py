#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_create_operations():
    """Тестируем операции создания подписок и экземпляров"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование операций создания ===\n")
    
    # Тест 1: Создание новой подписки
    print("1. Создание новой подписки:")
    subscription_data = {
        "name": "Тестовая подписка для создания",
        "amount": 250000,  # 2500 рублей
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
            print(f"✅ Подписка создана успешно")
            print(f"   ID: {data['subscription']['id']}")
            print(f"   Название: {data['subscription']['name']}")
            print(f"   Сумма: {data['subscription']['amount']} копеек")
            print(f"   Частота: {data['subscription']['frequency']}")
            
            # Сохраняем ID для создания экземпляра
            subscription_id = data['subscription']['id']
        else:
            print(f"❌ Ошибка: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Создание экземпляра подписки
    print("2. Создание экземпляра подписки:")
    instance_data = {
        "subscription_id": subscription_id,
        "amount": 250000,  # Может отличаться от базовой суммы
        "billing_time": "2025-07-25 15:30:00",
        "replenishment_time": "2025-07-25 16:00:00",
        "status": "progress"
    }
    
    try:
        response = requests.post(f"{base_url}/instances", json=instance_data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Экземпляр создан успешно")
            print(f"   ID: {data['instance']['id']}")
            print(f"   Подписка ID: {data['instance']['subscription_id']}")
            print(f"   Статус: {data['instance']['status']}")
            print(f"   Сумма: {data['instance']['amount']} копеек")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Проверка валидации при создании подписки
    print("3. Проверка валидации при создании подписки:")
    invalid_subscription_data = {
        "name": "",  # Пустое название
        "amount": -100,  # Отрицательная сумма
        "billing_time": "invalid-time",
        "replenishment_time": "16:00",
        "frequency": "invalid-frequency",
        "source": ""
    }
    
    try:
        response = requests.post(base_url, json=invalid_subscription_data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Корректно: API вернул ошибку валидации")
            print(f"   Ошибка: {data['error']}")
        else:
            print(f"⚠️ Неожиданный статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 4: Проверка валидации при создании экземпляра
    print("4. Проверка валидации при создании экземпляра:")
    invalid_instance_data = {
        "subscription_id": 99999,  # Несуществующий ID
        "amount": -100,
        "billing_time": "invalid-datetime",
        "replenishment_time": "2025-07-25 16:00:00",
        "status": "invalid-status"
    }
    
    try:
        response = requests.post(f"{base_url}/instances", json=invalid_instance_data)
        print(f"Статус: {response.status_code}")
        if response.status_code == 404:
            data = response.json()
            print(f"✅ Корректно: API вернул ошибку 'не найдено'")
            print(f"   Ошибка: {data['error']}")
        elif response.status_code == 400:
            data = response.json()
            print(f"✅ Корректно: API вернул ошибку валидации")
            print(f"   Ошибка: {data['error']}")
        else:
            print(f"⚠️ Неожиданный статус: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 5: Проверка списка подписок после создания
    print("5. Проверка списка подписок после создания:")
    try:
        response = requests.get(base_url)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            
            # Ищем созданную подписку
            created_subscription = None
            for sub in data['subscriptions']:
                if sub['name'] == "Тестовая подписка для создания":
                    created_subscription = sub
                    break
            
            if created_subscription:
                print(f"✅ Созданная подписка найдена в списке")
                print(f"   ID: {created_subscription['id']}")
                print(f"   Название: {created_subscription['name']}")
            else:
                print(f"⚠️ Созданная подписка не найдена в списке")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    test_create_operations() 