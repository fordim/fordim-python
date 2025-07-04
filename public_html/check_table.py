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
    
    print(f"Content-Type: text/html\n\n")
    print("<h1>Проверка структуры таблицы tasks</h1>")
    
    # Подключаемся к БД
    from sqlalchemy import create_engine, text
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL не найден в переменных окружения")
    engine = create_engine(database_url, echo=False)
    
    with engine.connect() as connection:
        # Проверяем структуру таблицы
        result = connection.execute(text("DESCRIBE tasks"))
        rows = result.fetchall()
        
        print("<h2>Структура таблицы tasks:</h2>")
        print("<table border='1' style='border-collapse: collapse;'>")
        print("<tr><th>Поле</th><th>Тип</th><th>Null</th><th>Ключ</th><th>По умолчанию</th><th>Дополнительно</th></tr>")
        
        for row in rows:
            print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>")
        
        print("</table>")
        
        # Проверяем данные
        result = connection.execute(text("SELECT * FROM tasks LIMIT 5"))
        rows = result.fetchall()
        
        print("<h2>Первые 5 записей:</h2>")
        if rows:
            print("<table border='1' style='border-collapse: collapse;'>")
            print("<tr><th>ID</th><th>Title</th><th>Description</th><th>Is Completed</th><th>Created At</th><th>Updated At</th></tr>")
            
            for row in rows:
                print(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>")
            
            print("</table>")
        else:
            print("<p>Таблица пуста</p>")
    
except Exception as e:
    print(f"Content-Type: text/html\n\n")
    print("<h1>Ошибка при проверке таблицы</h1>")
    print(f"<p style='color: red;'>❌ {str(e)}</p>")
    import traceback
    print(f"<pre>{traceback.format_exc()}</pre>") 