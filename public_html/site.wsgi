import os, sys

# Добавляем путь к виртуальному окружению
sys.path.insert(0, '/home/a0739858/python/lib/python3.13/site-packages')

# Добавляем путь к приложению
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Импортируем Flask и базу данных
    from flask import Flask, jsonify, request
    from database import SessionLocal, Task
    
    app = Flask(__name__)
    
    @app.route("/")
    def hello():
        return jsonify({"message": "Привет из Flask с базой данных!"})
    
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        try:
            db = SessionLocal()
            tasks = db.query(Task).all()
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": "completed" if task.is_completed else "pending",
                    "created_at": task.created_at.isoformat() if task.created_at else None
                })
            db.close()
            return jsonify({"tasks": task_list, "message": "Список задач из БД"})
        except Exception as e:
            return jsonify({"error": str(e), "message": "Ошибка подключения к БД"}), 500
    
    @app.route("/tasks", methods=["POST"])
    def create_task():
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
                "task": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "status": "completed" if new_task.is_completed else "pending"
                }
            })
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            db.close()
    
    @app.route("/test")
    def test():
        return jsonify({"status": "ok", "message": "Flask с БД работает!"})
    
    @app.route("/tasks-page")
    def tasks_page():
        return app.send_static_file('index.html')
    
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        data = request.get_json()
        db = SessionLocal()
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.title = data.get("title", task.title)
                task.description = data.get("description", task.description)
                task.is_completed = 1 if data.get("status") == "completed" else 0
                db.commit()
                return jsonify({"message": "Задача обновлена", "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": "completed" if task.is_completed else "pending"
                }})
            else:
                return jsonify({"error": "Задача не найдена"}), 404
        except Exception as e:
            db.rollback()
            return jsonify({"error": str(e)}), 400
        finally:
            db.close()
    
    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
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
    
    # Создаем WSGI приложение
    application = app
    
except Exception as e:
    # Fallback при ошибке
    def application(environ, start_response):
        status = '200 OK'
        output = f'Ошибка Flask: {str(e)}'.encode('utf-8')
        
        response_headers = [('Content-type', 'text/plain'),
                           ('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        
        return [output] 