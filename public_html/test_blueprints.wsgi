#!/usr/bin/env python3
import os, sys

# Добавляем путь к виртуальному окружению
sys.path.insert(0, '/home/a0739858/python/lib/python3.13/site-packages')

# Добавляем путь к приложению
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def application(environ, start_response):
    try:
        status = '200 OK'
        response_headers = [('Content-type', 'text/html')]
        
        output = "<h1>Тест Blueprint'ов</h1>".encode('utf-8')
        
        # Загружаем переменные окружения
        from dotenv import load_dotenv
        load_dotenv()
        output += "<p>✅ Переменные окружения загружены</p>".encode('utf-8')
        
        # Тестируем импорт Blueprint'ов
        try:
            from app.task_tracker import bp as task_bp
            output += "<p style='color: green;'>✅ task_tracker Blueprint импортирован</p>".encode('utf-8')
        except Exception as e:
            output += f"<p style='color: red;'>❌ Ошибка импорта task_tracker: {str(e)}</p>".encode('utf-8')
        
        try:
            from app.schedule import bp as schedule_bp
            output += "<p style='color: green;'>✅ schedule Blueprint импортирован</p>".encode('utf-8')
        except Exception as e:
            output += f"<p style='color: red;'>❌ Ошибка импорта schedule: {str(e)}</p>".encode('utf-8')
        
        # Создаем Flask приложение
        from app import create_app
        app = create_app()
        output += "<p>✅ Flask приложение создано</p>".encode('utf-8')
        
        # Проверяем маршруты
        routes = list(app.url_map.iter_rules())
        output += f"<h2>Все маршруты ({len(routes)}):</h2><ul>".encode('utf-8')
        for route in routes:
            output += f"<li>{route.rule} - {route.endpoint}</li>".encode('utf-8')
        output += "</ul>".encode('utf-8')
        
        # Проверяем Blueprint'ы в приложении
        output += "<h2>Зарегистрированные Blueprint'ы:</h2><ul>".encode('utf-8')
        for blueprint_name in app.blueprints:
            output += f"<li>{blueprint_name}</li>".encode('utf-8')
        output += "</ul>".encode('utf-8')
        
        response_headers.append(('Content-Length', str(len(output))))
        start_response(status, response_headers)
        return [output]
        
    except Exception as e:
        status = '500 INTERNAL SERVER ERROR'
        response_headers = [('Content-type', 'text/html')]
        output = f"<h1>Ошибка теста Blueprint'ов</h1><p style='color: red;'>{str(e)}</p>".encode('utf-8')
        response_headers.append(('Content-Length', str(len(output))))
        start_response(status, response_headers)
        return [output] 