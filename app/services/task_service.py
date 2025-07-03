from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.task import Task, TaskCreate, TaskUpdate
from app.db.session import SessionLocal

def get_db():
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tasks(db: Session) -> List[Task]:
    """Получить все задачи"""
    return db.query(Task).all()

def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Получить задачу по ID"""
    return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task_create: TaskCreate) -> Task:
    """Создать новую задачу"""
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        is_completed=task_create.is_completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Обновить задачу"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None
    
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    """Удалить задачу"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True