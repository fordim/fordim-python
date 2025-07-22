# Тесты проекта

Эта папка содержит все тесты для проекта.

## Структура

```
tests/
├── __init__.py
├── README.md
└── subscription/
    ├── __init__.py
    ├── README.md
    ├── test_datetime_api.py
    └── test_soon_payments.py
```

## Модули

### subscription/
Тесты для модуля подписок:
- API тесты с DateTime полями
- Тесты фильтра "скоро платить"
- Интеграционные тесты

## Запуск тестов

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите все тесты подписок
python tests/subscription/test_datetime_api.py
python tests/subscription/test_soon_payments.py
```

## Требования

- Python 3.11+
- Виртуальное окружение с установленными зависимостями
- Запущенный Flask сервер для API тестов
- База данных с тестовыми данными

## Добавление новых тестов

1. Создайте папку для нового модуля: `tests/your_module/`
2. Добавьте `__init__.py` и `README.md`
3. Создайте тестовые файлы с префиксом `test_`
4. Обновите этот README 