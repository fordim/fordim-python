from flask import jsonify
from app.schedule import bp

@bp.route('', methods=['GET'])
def get_schedule():
    """Получение расписания (заглушка)"""
    return jsonify({
        "message": "Фича Schedule в разработке",
        "events": []
    })

@bp.route('', methods=['POST'])
def create_event():
    """Создание события (заглушка)"""
    return jsonify({
        "message": "Фича Schedule в разработке",
        "status": "not_implemented"
    }) 