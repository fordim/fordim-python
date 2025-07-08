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
        
        # Фильтр "Скоро платить" — ближайший час
        if soon_filter == "true":
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            next_hour = (now + timedelta(hours=1)).strftime("%H:%M")
            query = query.filter(Subscription.billing_time >= now_str, Subscription.billing_time <= next_hour)
        
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
            filters_applied.append("скоро платить")
        
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
                "soon": soon_filter
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
        
        new_subscription = Subscription(
            name=data['name'],
            amount=data['amount'],
            billing_time=data['billing_time'],
            replenishment_time=data['replenishment_time'],
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
            subscription.billing_time = data['billing_time']
        if 'replenishment_time' in data:
            subscription.replenishment_time = data['replenishment_time']
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