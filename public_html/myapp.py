from flask import Flask, jsonify, request

app = Flask(__name__)
# Раскомментировать для получения traceback
# app.debug = True

@app.route("/")
def hello():
    return jsonify({"message": "Привет из Flask!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    # Здесь будет логика получения задач из БД
    return jsonify({"tasks": [], "message": "Список задач"})

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    # Здесь будет логика создания задачи
    return jsonify({"message": "Задача создана", "data": data})

@app.route("/test")
def test():
    return jsonify({"status": "ok", "message": "Flask работает!"})

if __name__ == "__main__":
   app.run() 