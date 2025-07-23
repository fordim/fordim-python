#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

def test_updated_interface():
    """Тестируем обновленный интерфейс с новой архитектурой"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование обновленного интерфейса ===\n")
    
    # Тест 1: Все подписки (Subscription)
    print("1. Все подписки (Subscription):")
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
    
    # Тест 2: К оплате (SubscriptionInstance в текущем месяце)
    print("2. К оплате (SubscriptionInstance в текущем месяце):")
    try:
        response = requests.get(f"{base_url}/instances/to-pay")
        print(f"URL: {base_url}/instances/to-pay")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['amount']} копеек, статус: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Создание экземпляра для текущего месяца
    print("3. Создание экземпляра для текущего месяца:")
    try:
        # Получаем ID первой подписки
        response = requests.get(f"{base_url}")
        if response.status_code == 200:
            data = response.json()
            if data['subscriptions']:
                subscription_id = data['subscriptions'][0]['id']
                
                # Создаем экземпляр для текущего месяца
                now = datetime.now()
                billing_time = now.replace(day=15, hour=10, minute=0, second=0, microsecond=0)
                replenishment_time = now.replace(day=15, hour=10, minute=30, second=0, microsecond=0)
                
                instance_data = {
                    "subscription_id": subscription_id,
                    "amount": 2500,
                    "billing_time": billing_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "replenishment_time": replenishment_time.strftime("%Y-%m-%d %H:%M:%S"),
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
    
    # Тест 4: Проверяем "К оплате" снова
    print("4. К оплате (после создания экземпляра):")
    try:
        response = requests.get(f"{base_url}/instances/to-pay")
        print(f"URL: {base_url}/instances/to-pay")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['amount']} копеек, статус: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 5: Оплаченные экземпляры
    print("5. Оплаченные экземпляры:")
    try:
        response = requests.get(f"{base_url}/instances?status=completed")
        print(f"URL: {base_url}/instances?status=completed")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['amount']} копеек, статус: {instance['status']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_updated_interface() 