from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base
from datetime import datetime
import enum

class FrequencyEnum(enum.Enum):
    """Enum для частоты повторения"""
    MONTH = "month"
    YEAR = "year"

class StatusEnum(enum.Enum):
    """Enum для статуса подписки"""
    COMPLETED = "completed"
    PROGRESS = "progress"

class Subscription(Base):
    """Модель подписки"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Имя подписки
    amount = Column(Integer, nullable=False)  # Сумма в копейках/центах
    billing_time = Column(DateTime, nullable=False)  # Время списания (полная дата с временем)
    replenishment_time = Column(DateTime, nullable=False)  # Время пополнения (полная дата с временем)
    frequency = Column(Enum(FrequencyEnum), nullable=False)  # Частота повторения
    source = Column(String(100), nullable=False)  # Откуда списывается
    status = Column(Enum(StatusEnum), default=StatusEnum.PROGRESS)  # Статус
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Преобразование в словарь для JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "billing_time": self.billing_time.isoformat() if self.billing_time is not None else None,
            "replenishment_time": self.replenishment_time.isoformat() if self.replenishment_time is not None else None,
            "frequency": self.frequency.value if self.frequency is not None else None,
            "source": self.source,
            "status": self.status.value if self.status is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None
        } 