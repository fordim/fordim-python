#!/usr/bin/env python3
"""
Тест подключения к базе данных
"""

import pymysql
from sqlalchemy import create_engine, text

def test_pymysql():
    """Тест прямого подключения через PyMySQL"""
    try:
        connection = pymysql.connect(
            host="141.8.192.169",
            port=3306,
            user="a0739858_fordim",
            password="HtPs84Xrt@wTaK",
            database="a0739858_fordim_web",
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            print(f"✅ PyMySQL подключение: {result}")
        
        connection.close()
        return True
    except Exception as e:
        print(f"❌ PyMySQL ошибка: {e}")
        return False

def test_sqlalchemy():
    """Тест подключения через SQLAlchemy"""
    try:
        database_url = "mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4"
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ SQLAlchemy подключение: {row}")
        
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Тестирование подключения к БД...")
    pymysql_ok = test_pymysql()
    sqlalchemy_ok = test_sqlalchemy()
    
    if pymysql_ok and sqlalchemy_ok:
        print("🎉 Все тесты прошли успешно!")
    else:
        print("⚠️ Есть проблемы с подключением к БД") 