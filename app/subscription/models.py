from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
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
    READY = "ready"

class Subscription(Base):
    """Модель подписки (шаблон)"""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Имя подписки
    amount = Column(Integer, nullable=False)  # Сумма в копейках/центах
    billing_time = Column(DateTime, nullable=False)  # Время списания (полная дата с временем)
    replenishment_time = Column(DateTime, nullable=False)  # Время пополнения (полная дата с временем)
    frequency = Column(Enum(FrequencyEnum), nullable=False)  # Частота повторения
    source = Column(String(100), nullable=False)  # Откуда списывается
    archived_at = Column(DateTime, nullable=True)  # Дата архивации
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с экземплярами подписок
    instances = relationship("SubscriptionInstance", back_populates="subscription", cascade="all, delete-orphan")
    
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
            "archived_at": self.archived_at.isoformat() if self.archived_at is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at is not None else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at is not None else None
        }

class SubscriptionInstance(Base):
    """Модель экземпляра подписки (конкретный месяц/период)"""
    __tablename__ = "subscription_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Сумма для этого экземпляра (может отличаться от базовой)
    billing_time = Column(DateTime, nullable=False)  # Время списания для этого экземпляра
    replenishment_time = Column(DateTime, nullable=False)  # Время пополнения для этого экземпляра
    status = Column(Enum(StatusEnum, values_callable=lambda obj: [e.value for e in obj]), default=StatusEnum.PROGRESS)  # Статус этого экземпляра
    completed_at = Column(DateTime, nullable=True)  # Когда перевели в статус completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связь с основной подпиской
    subscription = relationship("Subscription", back_populates="instances")
    
    def to_dict(self):
        """Преобразование в словарь для JSON"""
        def format_datetime(dt):
            """Безопасное форматирование даты"""
            if dt is None:
                return None
            if isinstance(dt, str):
                return dt
            return dt.isoformat()
        
        return {
            "id": self.id,
            "subscription_id": self.subscription_id,
            "amount": self.amount,
            "billing_time": format_datetime(self.billing_time),
            "replenishment_time": format_datetime(self.replenishment_time),
            "status": self.status.value if self.status is not None and hasattr(self.status, 'value') else (self.status if self.status is not None else None),
            "completed_at": format_datetime(self.completed_at),
            "created_at": format_datetime(self.created_at),
            "updated_at": format_datetime(self.updated_at),
            "subscription": self.subscription.to_dict() if self.subscription else None
        } 