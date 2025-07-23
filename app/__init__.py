from flask import Flask
from flask_cors import CORS
import atexit

def create_app():
    """Фабрика для создания Flask приложения"""
    app = Flask(__name__)
    
    # Настройки
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['JSON_AS_ASCII'] = False  # Поддержка русского языка
    
    # CORS для работы с фронтендом
    CORS(app)
    
    # Регистрируем фичи ПЕРЕД основными маршрутами
    try:
        from app.task_tracker import bp as task_bp
        app.register_blueprint(task_bp, url_prefix='/api/tasks')
        print("✅ Зарегистрирован Blueprint task_tracker")
    except Exception as e:
        print(f"❌ Ошибка регистрации task_tracker: {e}")
    
    try:
        from app.schedule import bp as schedule_bp
        app.register_blueprint(schedule_bp, url_prefix='/api/schedule')
        print("✅ Зарегистрирован Blueprint schedule")
    except Exception as e:
        print(f"❌ Ошибка регистрации schedule: {e}")
    
    try:
        from app.subscription import subscription_bp
        app.register_blueprint(subscription_bp, url_prefix='/api/subscription')
        print("✅ Зарегистрирован Blueprint subscription")
    except Exception as e:
        print(f"❌ Ошибка регистрации subscription: {e}")
    
    # Основные маршруты
    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)
    print("✅ Зарегистрирован Blueprint main")
    
    # Запуск планировщика задач
    try:
        from app.scheduler import test_scheduler
        test_scheduler.start()
        print("✅ Запущен тестовый планировщик задач")
        
        # Остановка планировщика при завершении приложения
        atexit.register(test_scheduler.stop)
        
    except Exception as e:
        print(f"❌ Ошибка запуска планировщика: {e}")
    
    return app 