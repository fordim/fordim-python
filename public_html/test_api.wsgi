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
        
        output = "<h1>Тест API задач</h1>".encode('utf-8')
        
        # Загружаем переменные окружения
        from dotenv import load_dotenv
        load_dotenv()
        output += "<p>✅ Переменные окружения загружены</p>".encode('utf-8')
        
        # Создаем Flask приложение
        from app import create_app
        app = create_app()
        output += "<p>✅ Flask приложение создано</p>".encode('utf-8')
        
        # Тестируем API через test_client
        with app.test_client() as client:
            # Тест главной страницы
            response = client.get('/')
            output += f"<p>Главная страница: {response.status_code}</p>".encode('utf-8')
            
            # Тест API задач
            response = client.get('/api/tasks')
            output += f"<p>API задач: {response.status_code}</p>".encode('utf-8')
            
            if response.status_code == 200:
                output += "<p style='color: green;'>✅ API работает!</p>".encode('utf-8')
                output += f"<pre>{response.data.decode('utf-8')}</pre>".encode('utf-8')
            else:
                output += "<p style='color: red;'>❌ API не работает</p>".encode('utf-8')
            
            # Тест health
            response = client.get('/health')
            output += f"<p>Health: {response.status_code}</p>".encode('utf-8')
        
        # Проверяем маршруты
        routes = list(app.url_map.iter_rules())
        output += f"<h2>Все маршруты ({len(routes)}):</h2><ul>".encode('utf-8')
        for route in routes:
            output += f"<li>{route.rule} - {route.endpoint}</li>".encode('utf-8')
        output += "</ul>".encode('utf-8')
        
        response_headers.append(('Content-Length', str(len(output))))
        start_response(status, response_headers)
        return [output]
        
    except Exception as e:
        status = '500 INTERNAL SERVER ERROR'
        response_headers = [('Content-type', 'text/html')]
        output = f"<h1>Ошибка API теста</h1><p style='color: red;'>{str(e)}</p>".encode('utf-8')
        response_headers.append(('Content-Length', str(len(output))))
        start_response(status, response_headers)
        return [output] 