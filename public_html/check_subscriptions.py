#!/usr/bin/env python3
"""
Скрипт для проверки структуры таблиц subscriptions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine
from sqlalchemy import text

def check_subscriptions_tables():
    """Проверяем структуру таблиц subscriptions"""
    
    print("Content-Type: text/html\n")
    print("<h1>Проверка структуры таблиц subscriptions</h1>")
    
    with engine.connect() as conn:
        # Проверяем таблицу subscriptions
        print("<h2>Структура таблицы subscriptions:</h2>")
        result = conn.execute(text("DESCRIBE subscriptions"))
        print("<table border='1' style='border-collapse: collapse;'>")
        print("<tr><th>Поле</th><th>Тип</th><th>Null</th><th>Ключ</th><th>По умолчанию</th><th>Дополнительно</th></tr>")
        for row in result:
            print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>")
        print("</table>")
        
        # Проверяем таблицу subscription_instances
        print("<h2>Структура таблицы subscription_instances:</h2>")
        result = conn.execute(text("DESCRIBE subscription_instances"))
        print("<table border='1' style='border-collapse: collapse;'>")
        print("<tr><th>Поле</th><th>Тип</th><th>Null</th><th>Ключ</th><th>По умолчанию</th><th>Дополнительно</th></tr>")
        for row in result:
            print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>")
        print("</table>")
        
        # Показываем данные из subscriptions
        print("<h2>Данные из таблицы subscriptions:</h2>")
        result = conn.execute(text("SELECT * FROM subscriptions LIMIT 5"))
        print("<table border='1' style='border-collapse: collapse;'>")
        print("<tr><th>ID</th><th>Name</th><th>Amount</th><th>Billing Time</th><th>Frequency</th><th>Source</th></tr>")
        for row in result:
            print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[5]}</td><td>{row[6]}</td></tr>")
        print("</table>")
        
        # Показываем данные из subscription_instances
        print("<h2>Данные из таблицы subscription_instances:</h2>")
        result = conn.execute(text("SELECT * FROM subscription_instances LIMIT 5"))
        print("<table border='1' style='border-collapse: collapse;'>")
        print("<tr><th>ID</th><th>Subscription ID</th><th>Amount</th><th>Status</th><th>Completed At</th></tr>")
        for row in result:
            print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>")
        print("</table>")

if __name__ == "__main__":
    check_subscriptions_tables() 