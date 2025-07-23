from flask import jsonify, request
from app.subscription.models import Subscription, SubscriptionInstance, FrequencyEnum, StatusEnum
from app.database import SessionLocal
from app.subscription import subscription_bp
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

@subscription_bp.route('', methods=['GET'])
def get_subscriptions():
    """Получение списка всех подписок с фильтрами"""
    db = SessionLocal()
    try:
        # Получаем параметры фильтрации из GET запроса
        frequency_filter = request.args.get('frequency')
        soon_filter = request.args.get('soon')
        month_filter = request.args.get('month')  # Фильтр по месяцу (YYYY-MM)
        
        # Начинаем с базового запроса - исключаем архивированные подписки
        query = db.query(Subscription).filter(Subscription.archived_at.is_(None))
        
        # Применяем фильтр по частоте
        if frequency_filter:
            try:
                frequency_enum = FrequencyEnum(frequency_filter)
                query = query.filter(Subscription.frequency == frequency_enum)
            except ValueError:
                return jsonify({"error": "Неверная частота. Допустимые значения: 'month', 'year'"}), 400
        

        
        # Фильтр по месяцу для оплаченных подписок
        if month_filter:
            try:
                # Парсим месяц в формате YYYY-MM
                year, month = map(int, month_filter.split('-'))
                
                # Начало указанного месяца
                start_of_month = datetime(year, month, 1, 0, 0, 0, 0)
                
                # Конец указанного месяца
                if month == 12:
                    end_of_month = datetime(year + 1, 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
                else:
                    end_of_month = datetime(year, month + 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
                
                query = query.filter(
                    Subscription.billing_time >= start_of_month,
                    Subscription.billing_time <= end_of_month
                )
            except (ValueError, IndexError):
                return jsonify({"error": "Неверный формат месяца. Используйте формат YYYY-MM (например: 2025-07)"}), 400
        
        # Выполняем запрос
        subscriptions = query.all()
        subscription_list = [sub.to_dict() for sub in subscriptions]
        
        # Формируем сообщение с информацией о применённых фильтрах
        filters_applied = []
        if frequency_filter:
            filters_applied.append(f"частота: {frequency_filter}")
        if soon_filter == "true":
            filters_applied.append("скоро платить (в текущем месяце)")
        if month_filter:
            # Форматируем месяц для отображения
            try:
                year, month = map(int, month_filter.split('-'))
                month_names = [
                    "январь", "февраль", "март", "апрель", "май", "июнь",
                    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
                ]
                month_name = month_names[month - 1]
                filters_applied.append(f"месяц: {month_name} {year}")
            except:
                filters_applied.append(f"месяц: {month_filter}")
        
        message = "Список подписок"
        if filters_applied:
            message += f" (фильтры: {', '.join(filters_applied)})"
        
        return jsonify({
            "subscriptions": subscription_list, 
            "message": message,
            "total_count": len(subscription_list),
            "filters": {
                "frequency": frequency_filter,
                "soon": soon_filter,
                "month": month_filter
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/archived', methods=['GET'])
def get_archived_subscriptions():
    """Получение списка архивированных подписок"""
    db = SessionLocal()
    try:
        # Получаем только архивированные подписки
        query = db.query(Subscription).filter(Subscription.archived_at.isnot(None))
        
        # Получаем параметры фильтрации
        frequency_filter = request.args.get('frequency')
        
        # Применяем фильтр по частоте
        if frequency_filter:
            try:
                frequency_enum = FrequencyEnum(frequency_filter)
                query = query.filter(Subscription.frequency == frequency_enum)
            except ValueError:
                return jsonify({"error": "Неверная частота. Допустимые значения: 'month', 'year'"}), 400
        
        subscriptions = query.all()
        subscription_list = [sub.to_dict() for sub in subscriptions]
        
        # Формируем сообщение с информацией о применённых фильтрах
        filters_applied = []
        if frequency_filter:
            filters_applied.append(f"частота: {frequency_filter}")
        
        message = "Список архивированных подписок"
        if filters_applied:
            message += f" (фильтры: {', '.join(filters_applied)})"
        
        return jsonify({
            "subscriptions": subscription_list, 
            "message": message,
            "total_count": len(subscription_list),
            "filters": {
                "frequency": frequency_filter
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/<int:subscription_id>', methods=['GET'])
def get_subscription(subscription_id):
    """Получение конкретной подписки"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if subscription:
            return jsonify({"subscription": subscription.to_dict(), "message": "Подписка найдена"})
        else:
            return jsonify({"error": "Подписка не найдена"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

def parse_datetime(datetime_str):
    """Парсинг строки даты в datetime объект"""
    if not datetime_str:
        return None
    
    # Пробуем разные форматы
    formats = [
        "%Y-%m-%dT%H:%M:%S",  # ISO format
        "%Y-%m-%d %H:%M:%S",  # MySQL format
        "%Y-%m-%dT%H:%M",     # ISO format без секунд
        "%Y-%m-%d %H:%M",     # MySQL format без секунд
        "%H:%M",              # Только время (добавим сегодняшнюю дату)
    ]
    
    for fmt in formats:
        try:
            if fmt == "%H:%M":
                # Для формата "HH:MM" добавляем сегодняшнюю дату
                time_parts = datetime_str.split(':')
                if len(time_parts) == 2:
                    hour, minute = int(time_parts[0]), int(time_parts[1])
                    today = datetime.now().date()
                    from datetime import time
                    return datetime.combine(today, time(hour, minute))
            else:
                return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Не удалось распарсить дату: {datetime_str}")

@subscription_bp.route('', methods=['POST'])
def create_subscription():
    """Создание новой подписки"""
    data = request.get_json()
    db = SessionLocal()
    try:
        # Валидация данных
        required_fields = ['name', 'amount', 'billing_time', 'replenishment_time', 'frequency', 'source']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Поле {field} обязательно"}), 400
        
        # Валидация frequency
        try:
            frequency = FrequencyEnum(data['frequency'])
        except ValueError:
            return jsonify({"error": "frequency должен быть 'month' или 'year'"}), 400
        
        # Парсинг дат
        try:
            billing_time = parse_datetime(data['billing_time'])
            replenishment_time = parse_datetime(data['replenishment_time'])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        new_subscription = Subscription(
            name=data['name'],
            amount=data['amount'],
            billing_time=billing_time,
            replenishment_time=replenishment_time,
            frequency=frequency,
            source=data['source']
        )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return jsonify({
            "success": True,
            "message": "Подписка создана",
            "subscription": new_subscription.to_dict()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@subscription_bp.route('/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    """Обновление подписки"""
    data = request.get_json()
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        # Обновляем только переданные поля
        if 'name' in data:
            subscription.name = data['name']
        if 'amount' in data:
            subscription.amount = data['amount']
        if 'billing_time' in data:
            try:
                subscription.billing_time = parse_datetime(data['billing_time'])
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        if 'replenishment_time' in data:
            try:
                subscription.replenishment_time = parse_datetime(data['replenishment_time'])
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        if 'frequency' in data:
            try:
                subscription.frequency = FrequencyEnum(data['frequency'])  # type: ignore
            except ValueError:
                return jsonify({"error": "frequency должен быть 'month' или 'year'"}), 400
        if 'source' in data:
            subscription.source = data['source']
        
        db.commit()
        return jsonify({"success": True, "message": "Подписка обновлена", "subscription": subscription.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()



@subscription_bp.route('/<int:subscription_id>/archive', methods=['POST'])
def archive_subscription(subscription_id):
    """Архивация подписки"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        if subscription.archived_at is not None:
            return jsonify({"error": "Подписка уже архивирована"}), 400
        
        subscription.archived_at = datetime.utcnow()
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "Подписка архивирована",
            "subscription": subscription.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/<int:subscription_id>/unarchive', methods=['POST'])
def unarchive_subscription(subscription_id):
    """Разархивация подписки"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        if subscription.archived_at is None:
            return jsonify({"error": "Подписка не архивирована"}), 400
        
        subscription.archived_at = None
        db.commit()
        
        return jsonify({
            "success": True,
            "message": "Подписка разархивирована",
            "subscription": subscription.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    """Удаление подписки"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        db.delete(subscription)
        db.commit()
        
        return jsonify({"message": "Подписка удалена"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close() 

# ============================================================================
# РОУТЫ ДЛЯ РАБОТЫ С ЭКЗЕМПЛЯРАМИ ПОДПИСОК (SubscriptionInstance)
# ============================================================================

@subscription_bp.route('/instances/to-pay', methods=['GET'])
def get_instances_to_pay():
    """Получение экземпляров подписок к оплате в текущем месяце"""
    db = SessionLocal()
    try:
        now = datetime.now()
        
        # Начало текущего месяца (1 число)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Конец текущего месяца (последний день месяца)
        if now.month == 12:
            end_of_month = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = now.replace(month=now.month + 1, day=1) - timedelta(days=1)
        end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Запрос экземпляров с billing_time в текущем месяце и статусом progress
        query = db.query(SubscriptionInstance).options(
            joinedload(SubscriptionInstance.subscription)
        ).filter(
            SubscriptionInstance.billing_time >= start_of_month,
            SubscriptionInstance.billing_time <= end_of_month,
            SubscriptionInstance.status == StatusEnum.PROGRESS
        )
        
        instances = query.all()
        instance_list = [instance.to_dict() for instance in instances]
        
        return jsonify({
            "instances": instance_list,
            "message": f"Экземпляры к оплате в {now.strftime('%B %Y')}",
            "total_count": len(instance_list),
            "period": {
                "start": start_of_month.isoformat(),
                "end": end_of_month.isoformat()
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/instances', methods=['GET'])
def get_subscription_instances():
    """Получение списка экземпляров подписок с фильтрами"""
    db = SessionLocal()
    try:
        # Получаем параметры фильтрации
        status_filter = request.args.get('status')
        subscription_id = request.args.get('subscription_id')
        month_filter = request.args.get('month')  # Фильтр по месяцу (YYYY-MM)
        
        # Начинаем с базового запроса
        query = db.query(SubscriptionInstance).options(joinedload(SubscriptionInstance.subscription))
        
        # Фильтр по статусу
        if status_filter:
            try:
                status_enum = StatusEnum(status_filter)
                query = query.filter(SubscriptionInstance.status == status_enum)
            except ValueError:
                return jsonify({"error": "Неверный статус. Допустимые значения: 'completed', 'progress'"}), 400
        
        # Фильтр по подписке
        if subscription_id:
            try:
                query = query.filter(SubscriptionInstance.subscription_id == int(subscription_id))
            except ValueError:
                return jsonify({"error": "Неверный ID подписки"}), 400
        
        # Фильтр по месяцу
        if month_filter:
            try:
                year, month = map(int, month_filter.split('-'))
                start_of_month = datetime(year, month, 1, 0, 0, 0, 0)
                if month == 12:
                    end_of_month = datetime(year + 1, 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
                else:
                    end_of_month = datetime(year, month + 1, 1, 23, 59, 59, 999999) - timedelta(days=1)
                
                query = query.filter(
                    SubscriptionInstance.created_at >= start_of_month,
                    SubscriptionInstance.created_at <= end_of_month
                )
            except (ValueError, IndexError):
                return jsonify({"error": "Неверный формат месяца. Используйте формат YYYY-MM"}), 400
        
        # Выполняем запрос
        instances = query.all()
        instance_list = [instance.to_dict() for instance in instances]
        
        # Формируем сообщение
        filters_applied = []
        if status_filter:
            filters_applied.append(f"статус: {status_filter}")
        if subscription_id:
            filters_applied.append(f"подписка ID: {subscription_id}")
        if month_filter:
            try:
                year, month = map(int, month_filter.split('-'))
                month_names = [
                    "январь", "февраль", "март", "апрель", "май", "июнь",
                    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
                ]
                month_name = month_names[month - 1]
                filters_applied.append(f"месяц: {month_name} {year}")
            except:
                filters_applied.append(f"месяц: {month_filter}")
        
        message = "Список экземпляров подписок"
        if filters_applied:
            message += f" (фильтры: {', '.join(filters_applied)})"
        
        return jsonify({
            "instances": instance_list,
            "message": message,
            "total_count": len(instance_list),
            "filters": {
                "status": status_filter,
                "subscription_id": subscription_id,
                "month": month_filter
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/instances/<int:instance_id>', methods=['GET'])
def get_subscription_instance(instance_id):
    """Получение конкретного экземпляра подписки"""
    db = SessionLocal()
    try:
        instance = db.query(SubscriptionInstance).options(
            joinedload(SubscriptionInstance.subscription)
        ).filter(SubscriptionInstance.id == instance_id).first()
        
        if instance:
            return jsonify({"instance": instance.to_dict(), "message": "Экземпляр подписки найден"})
        else:
            return jsonify({"error": "Экземпляр подписки не найден"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@subscription_bp.route('/instances', methods=['POST'])
def create_subscription_instance():
    """Создание нового экземпляра подписки"""
    data = request.get_json()
    db = SessionLocal()
    try:
        # Валидация данных
        required_fields = ['subscription_id', 'amount', 'billing_time', 'replenishment_time']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Поле {field} обязательно"}), 400
        
        # Проверяем существование подписки
        subscription = db.query(Subscription).filter(Subscription.id == data['subscription_id']).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        # Валидация статуса (если передан)
        status = StatusEnum.PROGRESS  # по умолчанию
        if 'status' in data:
            try:
                status = StatusEnum(data['status'])
            except ValueError:
                return jsonify({"error": "status должен быть 'completed' или 'progress'"}), 400
        
        # Парсинг дат
        try:
            billing_time = parse_datetime(data['billing_time'])
            replenishment_time = parse_datetime(data['replenishment_time'])
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        new_instance = SubscriptionInstance(
            subscription_id=data['subscription_id'],
            amount=data['amount'],
            billing_time=billing_time,
            replenishment_time=replenishment_time,
            status=status
        )
        
        db.add(new_instance)
        db.commit()
        db.refresh(new_instance)
        
        return jsonify({
            "success": True,
            "message": "Экземпляр подписки создан",
            "instance": new_instance.to_dict()
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@subscription_bp.route('/instances/<int:instance_id>/complete', methods=['POST'])
def complete_subscription_instance(instance_id):
    """Завершение экземпляра подписки"""
    db = SessionLocal()
    try:
        instance = db.query(SubscriptionInstance).filter(SubscriptionInstance.id == instance_id).first()
        if not instance:
            return jsonify({"error": "Экземпляр подписки не найден"}), 404
        
        instance.status = StatusEnum.COMPLETED
        instance.completed_at = datetime.utcnow()
        db.commit()
        
        return jsonify({
            "message": "Экземпляр подписки завершен", 
            "instance": instance.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@subscription_bp.route('/instances/<int:instance_id>', methods=['PUT'])
def update_subscription_instance(instance_id):
    """Обновление экземпляра подписки"""
    data = request.get_json()
    db = SessionLocal()
    try:
        instance = db.query(SubscriptionInstance).filter(SubscriptionInstance.id == instance_id).first()
        if not instance:
            return jsonify({"error": "Экземпляр подписки не найден"}), 404
        
        # Обновляем только переданные поля
        if 'amount' in data:
            instance.amount = data['amount']
        if 'billing_time' in data:
            try:
                instance.billing_time = parse_datetime(data['billing_time'])
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        if 'replenishment_time' in data:
            try:
                instance.replenishment_time = parse_datetime(data['replenishment_time'])
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        if 'status' in data:
            try:
                instance.status = StatusEnum(data['status'])
                if data['status'] == 'completed' and instance.completed_at is None:
                    instance.completed_at = datetime.utcnow()
                elif data['status'] == 'progress':
                    instance.completed_at = None
            except ValueError:
                return jsonify({"error": "status должен быть 'completed' или 'progress'"}), 400
        
        db.commit()
        return jsonify({
            "success": True, 
            "message": "Экземпляр подписки обновлен", 
            "instance": instance.to_dict()
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@subscription_bp.route('/instances/<int:instance_id>', methods=['DELETE'])
def delete_subscription_instance(instance_id):
    """Удаление экземпляра подписки"""
    db = SessionLocal()
    try:
        instance = db.query(SubscriptionInstance).filter(SubscriptionInstance.id == instance_id).first()
        if not instance:
            return jsonify({"error": "Экземпляр подписки не найден"}), 404
        
        db.delete(instance)
        db.commit()
        
        return jsonify({"message": "Экземпляр подписки удален"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close() 

@subscription_bp.route('/new-month', methods=['POST'])
def create_new_month_instances():
    """Создание экземпляров подписок для нового месяца"""
    try:
        from app.subscription.services import create_monthly_instances
        
        # Используем общий сервис
        result = create_monthly_instances()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close() 

@subscription_bp.route('/scheduler/jobs', methods=['GET'])
def get_scheduler_jobs():
    """Получение списка задач планировщика"""
    try:
        from app.scheduler import test_scheduler
        
        jobs = test_scheduler.get_jobs()
        job_list = []
        
        for job in jobs:
            job_list.append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return jsonify({
            'success': True,
            'jobs': job_list,
            'total_count': len(job_list)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_bp.route('/scheduler/run-test', methods=['POST'])
def run_test_instance_manual():
    """Ручной запуск создания тестового экземпляра"""
    try:
        from app.scheduler import test_scheduler
        
        # Вызываем функцию создания тестового экземпляра
        test_scheduler.create_test_instance()
        
        return jsonify({
            'success': True,
            'message': 'Тестовый экземпляр создан вручную'
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@subscription_bp.route('/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """Получение статуса планировщика"""
    try:
        from app.scheduler import test_scheduler
        
        jobs = test_scheduler.get_jobs()
        status = {
            'running': test_scheduler.scheduler.running,
            'total_jobs': len(jobs),
            'jobs': []
        }
        
        for job in jobs:
            status['jobs'].append({
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return jsonify({
            'success': True,
            'scheduler': status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400 