#!/usr/bin/env python3

import requests
import json

def test_subscription_colors():
    """Тестируем цветовое оформление подписок"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование цветового оформления подписок ===\n")
    
    try:
        response = requests.get(f"{base_url}")
        print(f"URL: {base_url}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено подписок: {data['total_count']}")
            print(f"Сообщение: {data['message']}")
            
            print("\nПодписки с их частотами:")
            for sub in data['subscriptions']:
                frequency_text = "месячная" if sub['frequency'] == 'month' else "годовая"
                color = "синяя" if sub['frequency'] == 'month' else "фиолетовая"
                print(f"  - {sub['name']}: {sub['amount']} копеек ({frequency_text}) - {color} рамка")
                
            # Проверяем, что есть и месячные, и годовые подписки
            month_count = sum(1 for sub in data['subscriptions'] if sub['frequency'] == 'month')
            year_count = sum(1 for sub in data['subscriptions'] if sub['frequency'] == 'year')
            
            print(f"\nСтатистика:")
            print(f"  - Месячных подписок: {month_count}")
            print(f"  - Годовых подписок: {year_count}")
            
            if month_count > 0 and year_count > 0:
                print("✅ Есть и месячные, и годовые подписки для тестирования цветов")
            else:
                print("⚠️ Нужны подписки обоих типов для полного тестирования")
                
        else:
            print(f"Ошибка: {response.text}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")

if __name__ == "__main__":
    test_subscription_colors() 