from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Настройки базы данных
DATABASE_URL = "mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4"

# Создаем движок
engine = create_engine(DATABASE_URL, echo=True)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Модель задачи
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    is_completed = Column(Integer, default=0)  # 0 = не завершено, 1 = завершено
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Создаем таблицы
Base.metadata.create_all(bind=engine)

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 