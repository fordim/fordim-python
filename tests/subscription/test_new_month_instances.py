#!/usr/bin/env python3

import requests
import json
from datetime import datetime, timedelta

def test_new_month_instances_api():
    """Тестируем API создания экземпляров нового месяца"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API создания экземпляров нового месяца ===\n")
    
    # Тест 1: Создание экземпляров для текущего месяца
    print("1. Создание экземпляров для текущего месяца:")
    try:
        response = requests.post(f"{base_url}/new-month")
        print(f"URL: {base_url}/new-month")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успех: {data['message']}")
            print(f"📊 Создано экземпляров: {data['created_count']}")
            print(f"⏭️ Пропущено подписок: {data['skipped_count']}")
            
            if data['created_instances']:
                print("\n📋 Созданные экземпляры:")
                for instance in data['created_instances']:
                    amount = instance['amount'] / 100
                    print(f"  • {instance['subscription_name']} - {amount}₽ ({instance['frequency']})")
            
            if data['skipped_subscriptions']:
                print("\n⏭️ Пропущенные подписки:")
                for sub in data['skipped_subscriptions']:
                    print(f"  • {sub['subscription_name']} - {sub['reason']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 2: Проверяем, что экземпляры действительно созданы
    print("2. Проверка созданных экземпляров:")
    try:
        response = requests.get(f"{base_url}/instances/to-pay")
        print(f"URL: {base_url}/instances/to-pay")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Всего экземпляров к оплате: {data['total_count']}")
            print(f"📝 Сообщение: {data['message']}")
            
            if data['instances']:
                print("\n📋 Экземпляры к оплате:")
                for instance in data['instances']:
                    amount = instance['amount'] / 100
                    billing_date = instance['billing_time'][:10]
                    print(f"  • {instance['subscription']['name']} - {amount}₽ ({billing_date})")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 3: Повторный вызов (должен пропустить уже созданные)
    print("3. Повторный вызов (проверка дублирования):")
    try:
        response = requests.post(f"{base_url}/new-month")
        print(f"URL: {base_url}/new-month")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Успех: {data['message']}")
            print(f"📊 Создано экземпляров: {data['created_count']}")
            print(f"⏭️ Пропущено подписок: {data['skipped_count']}")
            
            if data['created_count'] == 0:
                print("  ✓ Корректно: новые экземпляры не созданы (уже существуют)")
            
            if data['skipped_subscriptions']:
                print("\n⏭️ Пропущенные подписки:")
                for sub in data['skipped_subscriptions']:
                    print(f"  • {sub['subscription_name']} - {sub['reason']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    test_new_month_instances_api() 