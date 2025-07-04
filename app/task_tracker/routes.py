from flask import jsonify, request
from app.task_tracker.models import Task
from app.database import SessionLocal
from app.task_tracker import bp

@bp.route('', methods=['GET'])
def get_tasks():
    """Получение списка всех задач"""
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        task_list = [task.to_dict() for task in tasks]
        return jsonify({"tasks": task_list, "message": "Список задач"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@bp.route('', methods=['POST'])
def create_task():
    """Создание новой задачи"""
    data = request.get_json()
    db = SessionLocal()
    try:
        new_task = Task(
            title=data.get("title", ""),
            description=data.get("description", ""),
            is_completed=1 if data.get("status") == "completed" else 0
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return jsonify({
            "message": "Задача создана",
            "task": new_task.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновление задачи"""
    data = request.get_json()
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.is_completed = 1 if data.get("status") == "completed" else 0
            db.commit()
            return jsonify({"message": "Задача обновлена", "task": task.to_dict()})
        else:
            return jsonify({"error": "Задача не найдена"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаление задачи"""
    db = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return jsonify({"message": "Задача удалена"})
        else:
            return jsonify({"error": "Задача не найдена"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close() 