#!/usr/bin/env python3
"""
Тестовый скрипт для проверки соединения с базой данных
"""

import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

def test_pymysql_connection():
    """Тестируем прямое подключение через PyMySQL"""
    print("=== Тест прямого подключения PyMySQL ===")
    
    try:
        # Параметры подключения
        host = "141.8.192.169"
        port = 3306
        user = "a0739858_fordim"
        password = "HtPs84Xrt@wTaK"  # Обратите внимание: здесь @ без кодирования
        database = "a0739858_fordim_web"
        
        print(f"Подключаемся к: {host}:{port}")
        print(f"Пользователь: {user}")
        print(f"База данных: {database}")
        
        # Создаем подключение
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        print("✅ PyMySQL подключение успешно!")
        
        # Тестируем простой запрос
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            print(f"✅ Тестовый запрос выполнен: {result}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка PyMySQL подключения: {e}")
        return False

def test_sqlalchemy_connection():
    """Тестируем подключение через SQLAlchemy"""
    print("\n=== Тест SQLAlchemy подключения ===")
    
    try:
        # URL для SQLAlchemy (с кодированием @ в %40)
        database_url = "mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4"
        
        print(f"SQLAlchemy URL: {database_url}")
        
        # Создаем движок
        engine = create_engine(database_url, echo=True)
        
        # Тестируем подключение
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ SQLAlchemy тестовый запрос выполнен: {row}")
        
        print("✅ SQLAlchemy подключение успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка SQLAlchemy подключения: {e}")
        return False

def test_session():
    """Тестируем создание сессии"""
    print("\n=== Тест создания сессии ===")
    
    try:
        from app.db.session import SessionLocal
        
        # Создаем сессию
        session = SessionLocal()
        print("✅ Сессия создана успешно!")
        
        # Тестируем простой запрос
        result = session.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        print(f"✅ Запрос через сессию выполнен: {row}")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания сессии: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Начинаем тестирование соединения с базой данных...\n")
    
    # Тестируем все методы подключения
    pymysql_ok = test_pymysql_connection()
    sqlalchemy_ok = test_sqlalchemy_connection()
    session_ok = test_session()
    
    print("\n" + "="*50)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"PyMySQL: {'✅' if pymysql_ok else '❌'}")
    print(f"SQLAlchemy: {'✅' if sqlalchemy_ok else '❌'}")
    print(f"Session: {'✅' if session_ok else '❌'}")
    
    if all([pymysql_ok, sqlalchemy_ok, session_ok]):
        print("\n🎉 Все тесты прошли успешно! Соединение с БД работает корректно.")
    else:
        print("\n⚠️  Есть проблемы с соединением. Проверьте настройки.") 