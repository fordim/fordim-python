#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_new_subscription_structure():
    """Тестируем новую структуру API с SubscriptionInstance"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование новой структуры API ===\n")
    
    # Тест 1: Получение всех подписок (без статуса)
    print("1. Все подписки (без фильтра по статусу):")
    try:
        response = requests.get(f"{base_url}")
        print(f"URL: {base_url}")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for sub in data['subscriptions'][:3]:  # Показываем первые 3
                print(f"  - {sub['name']}: {sub['amount']} копеек")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Создание экземпляра подписки
    print("2. Создание экземпляра подписки:")
    try:
        # Сначала получаем ID первой подписки
        response = requests.get(f"{base_url}")
        if response.status_code == 200:
            data = response.json()
            if data['subscriptions']:
                subscription_id = data['subscriptions'][0]['id']
                
                # Создаем экземпляр
                instance_data = {
                    "subscription_id": subscription_id,
                    "amount": 2500,  # Может отличаться от базовой суммы
                    "billing_time": "2025-07-15 10:00:00",  # Конкретная дата для этого месяца
                    "replenishment_time": "2025-07-15 10:30:00",  # Конкретная дата для этого месяца
                    "status": "progress"
                }
                
                response = requests.post(f"{base_url}/instances", json=instance_data)
                print(f"URL: {base_url}/instances")
                print(f"Данные: {instance_data}")
                print(f"Статус: {response.status_code}")
                if response.status_code == 201:
                    data = response.json()
                    print(f"Создан экземпляр ID: {data['instance']['id']}")
                    print(f"Сообщение: {data['message']}")
                else:
                    print(f"Ошибка: {response.text}")
            else:
                print("Нет подписок для создания экземпляра")
        else:
            print(f"Ошибка получения подписок: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Получение экземпляров подписок
    print("3. Получение экземпляров подписок:")
    try:
        response = requests.get(f"{base_url}/instances")
        print(f"URL: {base_url}/instances")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - ID: {instance['id']}, Подписка: {instance['subscription']['name']}, Статус: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 4: Фильтр экземпляров по статусу
    print("4. Экземпляры со статусом 'progress':")
    try:
        response = requests.get(f"{base_url}/instances?status=progress")
        print(f"URL: {base_url}/instances?status=progress")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - ID: {instance['id']}, Статус: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_new_subscription_structure() 