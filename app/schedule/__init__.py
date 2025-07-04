from flask import Blueprint

bp = Blueprint('schedule', __name__)

# Импортируем маршруты в конце, чтобы избежать циклических импортов
from app.schedule import routes 