#!/usr/bin/env python3

import requests
import json
import time
from datetime import datetime

def test_scheduler_api():
    """Тестируем API планировщика задач"""
    base_url = "http://localhost:8000/api/subscription"
    
    print("=== Тестирование API планировщика задач ===\n")
    
    # Тест 1: Получение статуса планировщика
    print("1. Статус планировщика:")
    try:
        response = requests.get(f"{base_url}/scheduler/status")
        print(f"URL: {base_url}/scheduler/status")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Планировщик работает: {data['scheduler']['running']}")
            print(f"📊 Всего задач: {data['scheduler']['total_jobs']}")
            
            for job in data['scheduler']['jobs']:
                next_run = job['next_run'][:19] if job['next_run'] else 'Не запланировано'
                print(f"  • {job['name']}: следующий запуск в {next_run}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 2: Получение списка задач
    print("2. Список задач планировщика:")
    try:
        response = requests.get(f"{base_url}/scheduler/jobs")
        print(f"URL: {base_url}/scheduler/jobs")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Всего задач: {data['total_count']}")
            
            for job in data['jobs']:
                next_run = job['next_run'][:19] if job['next_run'] else 'Не запланировано'
                print(f"  • {job['name']} (ID: {job['id']})")
                print(f"    Следующий запуск: {next_run}")
                print(f"    Триггер: {job['trigger']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 3: Ручной запуск тестового экземпляра
    print("3. Ручной запуск создания тестового экземпляра:")
    try:
        response = requests.post(f"{base_url}/scheduler/run-test")
        print(f"URL: {base_url}/scheduler/run-test")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {data['message']}")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 4: Проверка созданных экземпляров
    print("4. Проверка экземпляров к оплате (после создания тестового):")
    try:
        response = requests.get(f"{base_url}/instances/to-pay")
        print(f"URL: {base_url}/instances/to-pay")
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"📊 Всего экземпляров к оплате: {data['total_count']}")
            
            # Показываем последние 3 экземпляра
            recent_instances = data['instances'][-3:] if data['instances'] else []
            if recent_instances:
                print("\n📋 Последние экземпляры:")
                for instance in recent_instances:
                    amount = instance['amount'] / 100
                    created = instance['created_at'][:19]
                    print(f"  • {instance['subscription']['name']} - {amount}₽ (создан: {created})")
        else:
            print(f"❌ Ошибка: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    
    print("\n" + "="*80 + "\n")
    
    # Тест 5: Мониторинг планировщика (ждем немного и проверяем снова)
    print("5. Мониторинг планировщика (через 10 секунд):")
    print("⏳ Ожидание 10 секунд для проверки работы планировщика...")
    time.sleep(10)
    
    try:
        response = requests.get(f"{base_url}/scheduler/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Планировщик все еще работает: {data['scheduler']['running']}")
            
            for job in data['scheduler']['jobs']:
                next_run = job['next_run'][:19] if job['next_run'] else 'Не запланировано'
                print(f"  • {job['name']}: следующий запуск в {next_run}")
        else:
            print(f"❌ Ошибка при проверке статуса: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    test_scheduler_api() 