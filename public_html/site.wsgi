import os, sys

# Добавляем путь к виртуальному окружению
sys.path.insert(0, '/home/a0739858/python/lib/python3.13/site-packages')

# Добавляем путь к приложению
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def application(environ, start_response):
    try:
        # Импортируем наше Flask приложение
        from app import create_app
        
        # Создаем приложение
        app = create_app()
        
        # Возвращаем WSGI приложение
        return app(environ, start_response)
        
    except Exception as e:
        # Fallback при ошибке
        status = '200 OK'
        output = f'Ошибка Flask: {str(e)}'.encode('utf-8')
        
        response_headers = [('Content-type', 'text/plain'),
                           ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        
        return [output] 