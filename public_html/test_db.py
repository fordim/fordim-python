#!/usr/bin/env python3
import os, sys

# Добавляем путь к виртуальному окружению
sys.path.insert(0, '/home/a0739858/python/lib/python3.13/site-packages')

# Добавляем путь к приложению
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

try:
    # Загружаем переменные окружения
    from dotenv import load_dotenv
    load_dotenv()
    
    # Проверяем переменную окружения
    database_url = os.getenv("DATABASE_URL")
    print(f"Content-Type: text/html\n\n")
    print("<h1>Тест подключения к БД</h1>")
    
    if not database_url:
        print("<p style='color: red;'>❌ DATABASE_URL не найден в переменных окружения!</p>")
        print("<p>Проверьте файл .env в корне проекта</p>")
        sys.exit(1)
    
    print(f"<p>✅ DATABASE_URL найден: {database_url[:50]}...</p>")
    
    # Пробуем подключиться к БД
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(database_url, echo=False)
    
    # Тестируем подключение
    with engine.connect() as connection:
        from sqlalchemy import text
        result = connection.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        if row and row[0] == 1:
            print("<p style='color: green;'>✅ Подключение к БД успешно!</p>")
        else:
            print("<p style='color: red;'>❌ Ошибка при выполнении тестового запроса</p>")
    
    # Проверяем таблицу tasks (отдельное соединение)
    try:
        with engine.connect() as connection2:
            result = connection2.execute(text("SELECT COUNT(*) as count FROM tasks"))
            row = result.fetchone()
            if row:
                print(f"<p style='color: green;'>✅ Таблица tasks найдена. Записей: {row[0]}</p>")
            else:
                print("<p style='color: orange;'>⚠️ Таблица tasks найдена, но результат пустой</p>")
    except Exception as e:
        print(f"<p style='color: orange;'>⚠️ Таблица tasks не найдена или ошибка: {str(e)}</p>")
    
    print("<h2>Переменные окружения:</h2>")
    print("<ul>")
    for key, value in os.environ.items():
        if 'DATABASE' in key or 'DB' in key:
            print(f"<li><strong>{key}:</strong> {value[:50]}...</li>")
    print("</ul>")
    
except Exception as e:
    print(f"Content-Type: text/html\n\n")
    print("<h1>Ошибка при тестировании БД</h1>")
    print(f"<p style='color: red;'>❌ {str(e)}</p>")
    print("<h2>Детали ошибки:</h2>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>") 