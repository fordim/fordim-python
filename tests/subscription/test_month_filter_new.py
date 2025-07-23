#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_month_filter_new_api():
    """Тестируем API фильтра по месяцам для экземпляров подписок"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API фильтра по месяцам (новая архитектура) ===\n")
    
    # Тест 1: Все оплаченные экземпляры подписок
    print("1. Все оплаченные экземпляры подписок:")
    try:
        response = requests.get(f"{base_url}/instances?status=completed")
        print(f"URL: {base_url}/instances?status=completed")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['billing_time']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Оплаченные экземпляры за июль 2025
    print("2. Оплаченные экземпляры за июль 2025:")
    try:
        response = requests.get(f"{base_url}/instances?status=completed&month=2025-07")
        print(f"URL: {base_url}/instances?status=completed&month=2025-07")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['billing_time']}")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Оплаченные экземпляры за июнь 2025 (должно быть 0)
    print("3. Оплаченные экземпляры за июнь 2025:")
    try:
        response = requests.get(f"{base_url}/instances?status=completed&month=2025-06")
        print(f"URL: {base_url}/instances?status=completed&month=2025-06")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            if data['total_count'] == 0:
                print("  ✓ Корректно: нет экземпляров за этот месяц")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 4: Неверный формат месяца
    print("4. Неверный формат месяца:")
    try:
        response = requests.get(f"{base_url}/instances?status=completed&month=invalid")
        print(f"URL: {base_url}/instances?status=completed&month=invalid")
        print(f"Статус: {response.status_code}")
        if response.status_code == 400:
            data = response.json()
            print(f"Ошибка: {data['error']}")
            print("  ✓ Корректно: API вернул ошибку валидации")
        else:
            print(f"Неожиданный статус: {response.status_code}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 5: Экземпляры к оплате в текущем месяце
    print("5. Экземпляры к оплате в текущем месяце:")
    try:
        response = requests.get(f"{base_url}/instances/to-pay")
        print(f"URL: {base_url}/instances/to-pay")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено экземпляров: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for instance in data['instances']:
                print(f"  - {instance['subscription']['name']}: {instance['billing_time']} (сумма: {instance['amount']})")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_month_filter_new_api() 