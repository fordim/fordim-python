from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import SessionLocal
from app.subscription.models import Subscription, SubscriptionInstance, StatusEnum, FrequencyEnum
from datetime import datetime, timedelta
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Настройка задач планировщика"""
        
        # Задача: Создание экземпляров для нового месяца (1-го числа каждого месяца в 9:00)
        self.scheduler.add_job(
            func=self.create_new_month_instances,
            trigger=CronTrigger(day=1, hour=9, minute=0),  # 1-го числа в 9:00
            id='new_month_instances',
            name='Создание экземпляров для нового месяца',
            replace_existing=True
        )
        
        # Задача: Логирование каждые 5 минут (для проверки работы планировщика)
        self.scheduler.add_job(
            func=self.log_scheduler_status,
            trigger=CronTrigger(minute='*/5'),  # Каждые 5 минут
            id='scheduler_status_log',
            name='Логирование статуса планировщика',
            replace_existing=True
        )
    
    def create_test_instance(self):
        """Создание тестового экземпляра подписки"""
        db = None
        try:
            logger.info("🕐 Запуск задачи: создание тестового экземпляра")
            
            # Создаем новое соединение с базой
            db = SessionLocal()
            
            # Получаем первую доступную подписку
            subscription = db.query(Subscription).filter(
                Subscription.archived_at.is_(None)
            ).first()
            
            if not subscription:
                logger.warning("❌ Нет доступных подписок для создания экземпляра")
                return
            
            # Создаем экземпляр с текущим временем
            now = datetime.utcnow()
            test_instance = SubscriptionInstance(
                subscription_id=subscription.id,
                amount=subscription.amount,
                billing_time=now + timedelta(hours=1),  # Через час
                replenishment_time=now + timedelta(hours=2),  # Через 2 часа
                status=StatusEnum.PROGRESS
            )
            
            db.add(test_instance)
            db.commit()
            
            logger.info(f"✅ Создан тестовый экземпляр: {subscription.name} - {subscription.amount/100}₽")
            
        except Exception as e:
            logger.error(f"❌ Ошибка при создании тестового экземпляра: {e}")
            if db:
                try:
                    db.rollback()
                except:
                    pass
        finally:
            if db:
                try:
                    db.close()
                except:
                    pass
    
    def create_new_month_instances(self):
        """Создание экземпляров подписок для нового месяца (как кнопка 'Новый месяц')"""
        try:
            logger.info("🕐 Запуск задачи: создание экземпляров для нового месяца")
            
            from app.subscription.services import create_monthly_instances
            
            # Используем общий сервис
            result = create_monthly_instances()
            
            # Логируем результат
            logger.info(f"✅ {result['message']}")
            if result['created_instances']:
                created_names = [inst['subscription_name'] for inst in result['created_instances']]
                logger.info(f"📋 Созданные экземпляры: {', '.join(created_names)}")
            if result['skipped_subscriptions']:
                skipped_names = [sub['subscription_name'] for sub in result['skipped_subscriptions']]
                logger.info(f"⏭️ Пропущенные: {', '.join(skipped_names)}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при создании экземпляров для нового месяца: {e}")
    
    def log_scheduler_status(self):
        """Логирование статуса планировщика"""
        try:
            jobs = self.scheduler.get_jobs()
            logger.info(f"📊 Статус планировщика: {len(jobs)} активных задач")
            
            for job in jobs:
                next_run = job.next_run_time.strftime('%H:%M:%S') if job.next_run_time else 'Не запланировано'
                logger.info(f"  • {job.name}: следующий запуск в {next_run}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка при логировании статуса: {e}")
    
    def start(self):
        """Запуск планировщика"""
        try:
            self.scheduler.start()
            logger.info("🚀 Тестовый планировщик запущен")
            
            # Показываем все задачи
            jobs = self.scheduler.get_jobs()
            logger.info(f"📋 Настроено задач: {len(jobs)}")
            for job in jobs:
                next_run = job.next_run_time.strftime('%H:%M:%S') if job.next_run_time else 'Не запланировано'
                logger.info(f"  • {job.name}: следующий запуск в {next_run}")
                
        except Exception as e:
            logger.error(f"❌ Ошибка запуска планировщика: {e}")
    
    def stop(self):
        """Остановка планировщика"""
        try:
            self.scheduler.shutdown()
            logger.info("🛑 Тестовый планировщик остановлен")
        except Exception as e:
            logger.error(f"❌ Ошибка остановки планировщика: {e}")
    
    def get_jobs(self):
        """Получение списка всех задач"""
        return self.scheduler.get_jobs()

# Создаем глобальный экземпляр планировщика
test_scheduler = TestScheduler() 