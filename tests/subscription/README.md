# Тесты для модуля подписок

Этот каталог содержит тесты для модуля подписок с новой архитектурой (Subscription + SubscriptionInstance).

## Структура тестов

### Актуальные тесты (новая архитектура):

1. **`test_new_structure.py`** - Основной тест новой архитектуры
   - Тестирует работу с Subscription (шаблоны подписок)
   - Тестирует создание и получение SubscriptionInstance
   - Проверяет фильтрацию экземпляров по статусу

2. **`test_interface.py`** - Тест обновленного интерфейса
   - Тестирует все вкладки интерфейса
   - Проверяет работу с экземплярами к оплате
   - Тестирует создание экземпляров для текущего месяца

3. **`test_colors.py`** - Тест цветового оформления
   - Проверяет отображение месячных и годовых подписок
   - Тестирует статистику по типам подписок

4. **`test_datetime_api.py`** - Тест работы с датами
   - Проверяет формат DateTime полей
   - Тестирует валидацию дат при создании экземпляров
   - Проверяет отображение дат в API

5. **`test_month_filter_new.py`** - Тест фильтра по месяцам (новая архитектура)
   - Тестирует фильтрацию экземпляров по месяцам
   - Проверяет работу с оплаченными экземплярами
   - Тестирует эндпоинт "к оплате"

6. **`test_create_operations.py`** - Тест операций создания
   - Тестирует создание новых подписок
   - Тестирует создание экземпляров подписок
   - Проверяет валидацию данных при создании

7. **`test_archive_operations.py`** - Тест операций архивации
   - Тестирует архивацию и разархивацию подписок
   - Проверяет фильтрацию активных и архивированных подписок
   - Тестирует валидацию операций архивации

8. **`test_new_month_instances.py`** - Тест создания экземпляров нового месяца
   - Тестирует автоматическое создание экземпляров для текущего месяца
   - Проверяет логику для месячных и годовых подписок
   - Тестирует защиту от дублирования экземпляров

### Удаленные тесты (устаревшие):

- ~~`test_month_filter.py`~~ - Удален, заменен на `test_month_filter_new.py`
- ~~`test_soon_payments.py`~~ - Удален, функциональность перенесена в `test_interface.py`

## Запуск тестов

```bash
# Запуск всех тестов
python tests/subscription/test_new_structure.py
python tests/subscription/test_interface.py
python tests/subscription/test_colors.py
python tests/subscription/test_datetime_api.py
python tests/subscription/test_month_filter_new.py
python tests/subscription/test_create_operations.py
python tests/subscription/test_archive_operations.py
python tests/subscription/test_new_month_instances.py

# Или запуск по одному
python tests/subscription/test_colors.py
```

## Новая архитектура

### Subscription (шаблон подписки):
- Основная сущность без статуса
- Содержит базовые параметры (название, сумма, частота, источник)
- Используется как шаблон для создания экземпляров

### SubscriptionInstance (экземпляр подписки):
- Конкретные экземпляры по месяцам
- Содержит статус (progress/completed)
- Имеет собственные даты billing_time и replenishment_time
- Связан с Subscription через foreign key

## API эндпоинты

### Subscription:
- `GET /api/subscription` - все активные подписки (исключая архивированные)
- `GET /api/subscription/archived` - все архивированные подписки
- `GET /api/subscription/{id}` - конкретная подписка
- `POST /api/subscription` - создание подписки
- `PUT /api/subscription/{id}` - обновление подписки
- `POST /api/subscription/{id}/archive` - архивация подписки
- `POST /api/subscription/{id}/unarchive` - разархивация подписки
- `DELETE /api/subscription/{id}` - удаление подписки

### SubscriptionInstance:
- `GET /api/subscription/instances` - все экземпляры
- `GET /api/subscription/instances/{id}` - конкретный экземпляр
- `POST /api/subscription/instances` - создание экземпляра
- `PUT /api/subscription/instances/{id}` - обновление экземпляра
- `DELETE /api/subscription/instances/{id}` - удаление экземпляра
- `POST /api/subscription/instances/{id}/complete` - завершение экземпляра
- `GET /api/subscription/instances/to-pay` - экземпляры к оплате в текущем месяце
- `POST /api/subscription/new-month` - создание экземпляров для нового месяца 