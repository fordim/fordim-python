#!/usr/bin/env python3

"""
Запуск только планировщика без Flask веб-сервера
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.scheduler import test_scheduler
import time
import logging

# Настраиваем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("🚀 Запуск планировщика без веб-сервера")
    print("📋 Задачи:")
    print("  • Логирование статуса каждые 5 минут")
    print("  • Создание экземпляров для нового месяца (1-го числа в 9:00)")
    print("\n💡 Для остановки нажмите Ctrl+C\n")
    
    try:
        # Запускаем планировщик
        test_scheduler.start()
        
        # Держим процесс живым
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Остановка планировщика...")
        test_scheduler.stop()
        print("✅ Планировщик остановлен")

if __name__ == "__main__":
    main() 