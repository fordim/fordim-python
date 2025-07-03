from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import get_tasks, get_task, create_task, update_task, delete_task, get_db

router = APIRouter()

@router.get("/tasks", response_model=List[TaskResponse])
def read_tasks(db: Session = Depends(get_db)):
    """Получить все задачи"""
    return get_tasks(db)

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Получить задачу по ID"""
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.post("/tasks", response_model=TaskResponse)
def add_task(task_create: TaskCreate, db: Session = Depends(get_db)):
    """Создать новую задачу"""
    return create_task(db, task_create)

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    """Обновить задачу"""
    updated = update_task(db, task_id, task_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return updated

@router.delete("/tasks/{task_id}")
def remove_task(task_id: int, db: Session = Depends(get_db)):
    """Удалить задачу"""
    deleted = delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"detail": "Задача удалена"}