#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

def test_soon_payments_api():
    """Тестируем API для подписок в текущем месяце"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API 'Скоро платить' (в текущем месяце) ===\n")
    
    # Тест 1: Подписки в текущем месяце
    print("1. Подписки в текущем месяце:")
    try:
        response = requests.get(f"{base_url}?soon=true")
        print(f"URL: {base_url}?soon=true")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for sub in data['subscriptions']:
                print(f"  - {sub['name']}: {sub['billing_time']} (сумма: {sub['amount']})")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Комбинированный фильтр - подписки в текущем месяце + только месячные
    print("2. Месячные подписки в текущем месяце:")
    try:
        response = requests.get(f"{base_url}?soon=true&frequency=month")
        print(f"URL: {base_url}?soon=true&frequency=month")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for sub in data['subscriptions']:
                print(f"  - {sub['name']}: {sub['billing_time']} (сумма: {sub['amount']})")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Комбинированный фильтр - подписки в текущем месяце + только годовые
    print("3. Годовые подписки в текущем месяце:")
    try:
        response = requests.get(f"{base_url}?soon=true&frequency=year")
        print(f"URL: {base_url}?soon=true&frequency=year")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            for sub in data['subscriptions']:
                print(f"  - {sub['name']}: {sub['billing_time']} (сумма: {sub['amount']})")
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_soon_payments_api() 