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
    billing_time = Column(String(50), nullable=False)  # Время списания (например: "15:30")
    replenishment_time = Column(String(50), nullable=False)  # Время пополнения (например: "15:30")
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
            "billing_time": self.billing_time,
            "replenishment_time": self.replenishment_time,
            "frequency": self.frequency.value if self.frequency is not None else None,
            "source": self.source,
            "status": self.status.value if self.status is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None
        } 