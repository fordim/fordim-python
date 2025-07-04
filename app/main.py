from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import time_tracker

app = FastAPI()

# Подключаем статические файлы
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(time_tracker.router, prefix="/time-tracker", tags=["time-tracker"])

@app.get("/")
def root():
    return {"message": "Привет из FastAPI!"}

@app.get("/tasks")
def tasks_page():
    """Страница для управления задачами"""
    return FileResponse("app/static/index.html")
