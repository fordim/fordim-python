from flask import jsonify, request
from app.subscription.models import Subscription, FrequencyEnum, StatusEnum
from app.database import SessionLocal
from app.subscription import subscription_bp
from datetime import datetime, timedelta

@subscription_bp.route('', methods=['GET'])
def get_subscriptions():
    """Получение списка всех подписок с фильтрами"""
    db = SessionLocal()
    try:
        # Получаем параметры фильтрации из GET запроса
        status_filter = request.args.get('status')
        frequency_filter = request.args.get('frequency')
        soon_filter = request.args.get('soon')
        month_filter = request.args.get('month')  # Фильтр по месяцу (YYYY-MM)
        
        # Начинаем с базового запроса
        query = db.query(Subscription)
        
        # Применяем фильтр по статусу
        if status_filter:
            try:
                status_enum = StatusEnum(status_filter)
                query = query.filter(Subscription.status == status_enum)
            except ValueError:
                return jsonify({"error": "Неверный статус. Допустимые значения: 'completed', 'progress'"}), 400
        
        # Применяем фильтр по частоте
        if frequency_filter:
            try:
                frequency_enum = FrequencyEnum(frequency_filter)
                query = query.filter(Subscription.frequency == frequency_enum)
            except ValueError:
                return jsonify({"error": "Неверная частота. Допустимые значения: 'month', 'year'"}), 400
        
        # Фильтр "Скоро платить" — подписки в текущем месяце
        if soon_filter == "true":
            now = datetime.now()
            
            # Начало текущего месяца (1 число)
            start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            # Конец текущего месяца (последний день месяца)
            if now.month == 12:
                end_of_month = now.replace(year=now.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end_of_month = now.replace(month=now.month + 1, day=1) - timedelta(days=1)
            end_of_month = end_of_month.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            query = query.filter(
                Subscription.billing_time >= start_of_month,
                Subscription.billing_time <= end_of_month,
                Subscription.status == StatusEnum.PROGRESS  # Только активные подписки
            )
        
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
        if status_filter:
            filters_applied.append(f"статус: {status_filter}")
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
                "status": status_filter,
                "frequency": frequency_filter,
                "soon": soon_filter,
                "month": month_filter
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
        
        # Валидация status (если передан)
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
        
        new_subscription = Subscription(
            name=data['name'],
            amount=data['amount'],
            billing_time=billing_time,
            replenishment_time=replenishment_time,
            frequency=frequency,
            source=data['source'],
            status=status
        )
        
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        
        return jsonify({
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
        if 'status' in data:
            try:
                subscription.status = StatusEnum(data['status'])  # type: ignore
            except ValueError:
                return jsonify({"error": "status должен быть 'completed' или 'progress'"}), 400
        
        db.commit()
        return jsonify({"success": True, "message": "Подписка обновлена", "subscription": subscription.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@subscription_bp.route('/<int:subscription_id>/complete', methods=['POST'])
def complete_subscription(subscription_id):
    """Завершение подписки"""
    db = SessionLocal()
    try:
        subscription = db.query(Subscription).filter(Subscription.id == subscription_id).first()
        if not subscription:
            return jsonify({"error": "Подписка не найдена"}), 404
        
        subscription.status = StatusEnum.COMPLETED  # type: ignore
        db.commit()
        
        return jsonify({"message": "Подписка завершена", "subscription": subscription.to_dict()})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 400
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