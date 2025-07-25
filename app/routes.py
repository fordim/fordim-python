from flask import Blueprint, jsonify, send_from_directory

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Главная страница"""
    return jsonify({
        "message": "Добро пожаловать в Flask приложение!",
        "features": [
            {"name": "task_tracker", "url": "/api/tasks", "page": "/tasks-page"},
            {"name": "schedule", "url": "/api/schedule"},
            {"name": "subscription", "url": "/api/subscription", "page": "/subscriptions-page"}
        ]
    })

@bp.route('/health')
def health():
    """Проверка здоровья приложения"""
    return jsonify({"status": "ok", "message": "Приложение работает"})

@bp.route('/tasks-page')
def tasks_page():
    """Страница управления задачами"""
    return send_from_directory('static', 'index.html')

@bp.route('/subscriptions-page')
def subscriptions_page():
    """Страница управления подписками"""
    return send_from_directory('static', 'subscriptions.html')

@bp.route('/debug/routes')
def debug_routes():
    """Отладка - показать все доступные маршруты"""
    from flask import current_app
    routes = []
    for rule in current_app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods) if rule.methods else [],
            'rule': str(rule)
        })
    return jsonify({"routes": routes}) 