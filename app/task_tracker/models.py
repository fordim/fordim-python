from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base
from datetime import datetime

class Task(Base):
    """Модель задачи"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    is_completed = Column(Integer, default=0)  # 0 = не завершено, 1 = завершено
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Преобразование в словарь для JSON"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": "completed" if self.is_completed else "pending",
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        } 