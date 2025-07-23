#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def test_archive_operations():
    """Тестируем операции архивации подписок"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование операций архивации ===\n")
    
    # Тест 1: Создание подписки для архивации
    print("1. Создание подписки для архивации:")
    subscription_data = {
        "name": "Тестовая подписка для архивации",
        "amount": 300000,  # 3000 рублей
        "billing_time": "16:30",
        "replenishment_time": "17:00",
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
            
            # Сохраняем ID для архивации
            subscription_id = data['subscription']['id']
        else:
            print(f"❌ Ошибка: {response.text}")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return
    
    print("\n" + "="*60 + "\n")
    
    # Тест 2: Проверка, что подписка есть в списке активных
    print("2. Проверка списка активных подписок:")
    try:
        response = requests.get(base_url)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено активных подписок: {data['total_count']}")
            
            # Ищем созданную подписку
            found = False
            for sub in data['subscriptions']:
                if sub['name'] == "Тестовая подписка для архивации":
                    found = True
                    print(f"✅ Подписка найдена в активных (ID: {sub['id']})")
                    break
            
            if not found:
                print("⚠️ Подписка не найдена в активных")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 3: Архивация подписки
    print("3. Архивация подписки:")
    try:
        response = requests.post(f"{base_url}/{subscription_id}/archive")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Подписка архивирована успешно")
            print(f"   Сообщение: {data['message']}")
            print(f"   Дата архивации: {data['subscription']['archived_at']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 4: Проверка, что подписка исчезла из активных
    print("4. Проверка, что подписка исчезла из активных:")
    try:
        response = requests.get(base_url)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено активных подписок: {data['total_count']}")
            
            # Ищем архивированную подписку
            found = False
            for sub in data['subscriptions']:
                if sub['name'] == "Тестовая подписка для архивации":
                    found = True
                    print(f"⚠️ Подписка все еще в активных (ID: {sub['id']})")
                    break
            
            if not found:
                print("✅ Подписка исчезла из активных (корректно)")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 5: Проверка архивированных подписок
    print("5. Проверка списка архивированных подписок:")
    try:
        response = requests.get(f"{base_url}/archived")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено архивированных подписок: {data['total_count']}")
            
            # Ищем архивированную подписку
            found = False
            for sub in data['subscriptions']:
                if sub['name'] == "Тестовая подписка для архивации":
                    found = True
                    print(f"✅ Подписка найдена в архиве (ID: {sub['id']})")
                    print(f"   Дата архивации: {sub['archived_at']}")
                    break
            
            if not found:
                print("⚠️ Подписка не найдена в архиве")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 6: Разархивация подписки
    print("6. Разархивация подписки:")
    try:
        response = requests.post(f"{base_url}/{subscription_id}/unarchive")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Подписка разархивирована успешно")
            print(f"   Сообщение: {data['message']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 7: Проверка, что подписка вернулась в активные
    print("7. Проверка, что подписка вернулась в активные:")
    try:
        response = requests.get(base_url)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Найдено активных подписок: {data['total_count']}")
            
            # Ищем разархивированную подписку
            found = False
            for sub in data['subscriptions']:
                if sub['name'] == "Тестовая подписка для архивации":
                    found = True
                    print(f"✅ Подписка вернулась в активные (ID: {sub['id']})")
                    break
            
            if not found:
                print("⚠️ Подписка не вернулась в активные")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*60 + "\n")
    
    # Тест 8: Проверка валидации архивации
    print("8. Проверка валидации архивации:")
    try:
        # Пытаемся архивировать уже архивированную подписку
        response = requests.post(f"{base_url}/{subscription_id}/archive")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Подписка снова архивирована")
            
            # Пытаемся архивировать еще раз
            response = requests.post(f"{base_url}/{subscription_id}/archive")
            print(f"Повторная архивация - Статус: {response.status_code}")
            if response.status_code == 400:
                data = response.json()
                print(f"✅ Корректно: API вернул ошибку валидации")
                print(f"   Ошибка: {data['error']}")
            else:
                print(f"⚠️ Неожиданный статус: {response.status_code}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    test_archive_operations() 