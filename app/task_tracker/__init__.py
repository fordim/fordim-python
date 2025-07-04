from flask import Blueprint

bp = Blueprint('task_tracker', __name__)

# Импортируем маршруты в конце, чтобы избежать циклических импортов
from app.task_tracker import routes 