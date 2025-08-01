"""
Сервисы для работы с подписками
"""

from datetime import datetime, timedelta
from app.database import SessionLocal
from app.subscription.models import Subscription, SubscriptionInstance, StatusEnum, FrequencyEnum
import logging

logger = logging.getLogger(__name__)

def create_monthly_instances(db_session=None):
    """
    Создание экземпляров подписок для текущего месяца
    
    Args:
        db_session: Сессия базы данных. Если None, создается новая сессия.
    
    Returns:
        dict: Результат операции с информацией о созданных и пропущенных экземплярах
    """
    should_close_session = False
    if db_session is None:
        db_session = SessionLocal()
        should_close_session = True
    
    try:
        # Получаем текущий месяц
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year
        
        # Начало и конец текущего месяца
        start_of_month = datetime(current_year, current_month, 1, 0, 0, 0, 0)
        if current_month == 12:
            end_of_month = datetime(current_year + 1, 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
        else:
            end_of_month = datetime(current_year, current_month + 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
        
        # Получаем все неархивированные подписки
        subscriptions = db_session.query(Subscription).filter(Subscription.archived_at.is_(None)).all()
        
        created_instances = []
        skipped_subscriptions = []
        
        for subscription in subscriptions:
            should_create = False
            new_billing_time = None
            new_replenishment_time = None
            
            if subscription.frequency == FrequencyEnum.MONTH: # type: ignore
                # Для месячных подписок - создаем экземпляр каждый месяц
                should_create = True
                # Берем время из подписки, но меняем на текущий месяц
                new_billing_time = start_of_month.replace(
                    hour=subscription.billing_time.hour,
                    minute=subscription.billing_time.minute,
                    second=subscription.billing_time.second
                )
                new_replenishment_time = start_of_month.replace(
                    hour=subscription.replenishment_time.hour,
                    minute=subscription.replenishment_time.minute,
                    second=subscription.replenishment_time.second
                )
                
            elif subscription.frequency == FrequencyEnum.YEAR:  # type: ignore
                # Для годовых подписок - создаем только если billing_time в текущем месяце
                if subscription.billing_time.month == current_month:
                    should_create = True
                    # Берем время из подписки, но меняем год на текущий
                    new_billing_time = subscription.billing_time.replace(year=current_year)
                    new_replenishment_time = subscription.replenishment_time.replace(year=current_year)
            
            if should_create:
                # Проверяем, не создан ли уже экземпляр для этой подписки в текущем месяце
                existing_instance = db_session.query(SubscriptionInstance).filter(
                    SubscriptionInstance.subscription_id == subscription.id,
                    SubscriptionInstance.billing_time >= start_of_month,
                    SubscriptionInstance.billing_time <= end_of_month
                ).first()
                
                if existing_instance:
                    skipped_subscriptions.append({
                        "subscription_name": subscription.name,
                        "reason": "Экземпляр уже создан для текущего месяца"
                    })
                else:
                    # Создаем новый экземпляр
                    new_instance = SubscriptionInstance(
                        subscription_id=subscription.id,
                        amount=subscription.amount,
                        billing_time=new_billing_time,
                        replenishment_time=new_replenishment_time,
                        status=StatusEnum.PROGRESS
                    )
                    db_session.add(new_instance)
                    created_instances.append({
                        "subscription_name": subscription.name,
                        "amount": subscription.amount,
                        "billing_time": new_billing_time.isoformat(), # type: ignore
                        "frequency": subscription.frequency.value
                    })
        
        # Сохраняем изменения
        db_session.commit()
        
        # Формируем сообщение
        month_names = [
            "январь", "февраль", "март", "апрель", "май", "июнь",
            "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
        ]
        month_name = month_names[current_month - 1]
        
        result = {
            "success": True,
            "message": f"Создано экземпляров для {month_name} {current_year}",
            "created_count": len(created_instances),
            "skipped_count": len(skipped_subscriptions),
            "created_instances": created_instances,
            "skipped_subscriptions": skipped_subscriptions,
            "month_name": month_name,
            "current_year": current_year
        }
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Ошибка при создании экземпляров для нового месяца: {e}")
        if should_close_session and db_session:
            try:
                db_session.rollback()
            except:
                pass
        raise
    finally:
        if should_close_session and db_session:
            try:
                db_session.close()
            except:
                pass 