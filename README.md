# Fordim Python Project

Учебный проект на Python с Flask, SQLAlchemy и MySQL. Архитектура похожа на Symfony Framework.

## 🏗️ Структура проекта

```
fordim-python/
├── app/                    # Основное приложение
│   ├── __init__.py        # Фабрика Flask приложения
│   ├── routes.py          # Основные маршруты
│   ├── database.py        # Подключение к БД
│   ├── task_tracker/      # Фича: управление задачами
│   │   ├── __init__.py
│   │   ├── models.py      # Модель Task
│   │   └── routes.py      # API маршруты
│   └── schedule/          # Фича: планировщик (заглушка)
│       ├── __init__.py
│       └── routes.py
├── alembic/               # Миграции базы данных
├── public_html/           # Файлы для сервера
│   ├── site.wsgi         # WSGI точка входа
│   ├── .htaccess         # Настройки Apache
│   └── static/           # Статические файлы
├── run.py                # Точка входа для разработки
├── requirements.txt      # Зависимости
└── alembic.ini          # Конфигурация Alembic
```

## 🚀 Быстрый старт

### Локальная разработка

1. **Активируйте виртуальное окружение:**
   ```bash
   source venv/bin/activate
   ```

2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта:
   ```env
   # База данных
   DATABASE_URL=mysql+pymysql://username:password@host:port/database?charset=utf8mb4
   
   # Flask настройки
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=your-secret-key-here-change-in-production
   
   # Дополнительные настройки
   DEBUG=True
   ```

4. **Запустите миграции:**
   ```bash
   alembic upgrade head
   ```

5. **Запустите приложение:**
   ```bash
   python run.py
   ```

6. **Откройте в браузере:**
   - Веб-интерфейс: http://localhost:8000/tasks-page
   - API: http://localhost:8000/api/tasks

### Деплой на сервер

1. **Загрузите файлы в `public_html/`**
2. **Настройте базу данных MySQL**
3. **Примените миграции:**
   ```bash
   alembic upgrade head
   ```

## 📋 API Endpoints

### Задачи (`/api/tasks`)

- `GET /api/tasks` - Получить список задач
- `POST /api/tasks` - Создать задачу
- `PUT /api/tasks/{id}` - Обновить задачу
- `DELETE /api/tasks/{id}` - Удалить задачу

### Основные маршруты

- `GET /` - Главная страница
- `GET /tasks-page` - Веб-интерфейс управления задачами
- `GET /health` - Проверка здоровья приложения
- `GET /debug/routes` - Список всех маршрутов

## 🛠️ Технологии

- **Flask** - веб-фреймворк (аналог Symfony)
- **SQLAlchemy** - ORM (аналог Doctrine)
- **Alembic** - миграции БД (аналог Doctrine Migrations)
- **MySQL** - база данных
- **Blueprint'ы** - модульная архитектура (аналог Bundle'ов в Symfony)

## 🏛️ Архитектура

Проект использует модульную архитектуру с Blueprint'ами:

- **task_tracker** - управление задачами
- **schedule** - планировщик (в разработке)
- **main** - основные маршруты

Каждая фича (Blueprint) содержит:
- Модели данных
- API маршруты
- Бизнес-логику

## 📝 Примеры использования

### Создание задачи через API

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Новая задача",
    "description": "Описание задачи",
    "status": "pending"
  }'
```

### Получение списка задач

```bash
curl http://localhost:8000/api/tasks
```

## 🔧 Разработка

### Добавление новой фичи

1. Создайте папку в `app/` (например, `app/users/`)
2. Создайте `__init__.py` с Blueprint
3. Добавьте модели в `models.py`
4. Добавьте маршруты в `routes.py`
5. Зарегистрируйте Blueprint в `app/__init__.py`

### Создание миграции

```bash
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
```

## 📚 Сравнение с Symfony

| Symfony | Flask (наш проект) |
|---------|-------------------|
| Bundle | Blueprint |
| Entity | SQLAlchemy Model |
| Controller | Route function |
| Doctrine | SQLAlchemy |
| Doctrine Migrations | Alembic |
| AppKernel | create_app() |
| Service Container | Flask extensions |

## 🎯 Цели проекта

- Изучение Python и Flask
- Понимание веб-разработки
- Освоение работы с базами данных
- Изучение архитектурных паттернов
- Подготовка к созданию микросервисов 