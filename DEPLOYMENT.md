# Инструкция по развертыванию FastAPI приложения

## 1. Подготовка сервера

### Установка Python и зависимостей
```bash
# Установка Python 3.11+ (если не установлен)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## 2. Настройка базы данных

### Создание .env файла
Создайте файл `.env` в корне проекта:
```env
DATABASE_URL=mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4
```

### Применение миграций
```bash
# Инициализация Alembic (если еще не сделано)
alembic init alembic

# Применение миграций
alembic upgrade head
```

## 3. Настройка веб-сервера

### Вариант 1: Через .htaccess (для shared hosting)
Файл `.htaccess` уже настроен для работы с `main.py`.

### Вариант 2: Через systemd (для VPS)
Создайте файл `/etc/systemd/system/fastapi.service`:
```ini
[Unit]
Description=FastAPI application
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/app/venv/bin"
ExecStart=/path/to/your/app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi
sudo systemctl start fastapi
```

### Вариант 3: Через Nginx + Gunicorn
Установите Gunicorn:
```bash
pip install gunicorn
```

Создайте файл `gunicorn.conf.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
```

Запуск:
```bash
gunicorn -c gunicorn.conf.py app.main:app
```

## 4. Проверка работы

### Тест API
```bash
curl http://your-domain.com/
curl http://your-domain.com/tasks/
```

### Тест создания задачи
```bash
curl -X POST "http://your-domain.com/tasks/" \
  -H "Content-Type: application/json" \
  -d '{"title": "Тест", "description": "Описание", "status": "pending"}'
```

## 5. Структура файлов на сервере

```
public_html/
├── .htaccess              # Настройки Apache
├── main.py                # WSGI входная точка
├── requirements.txt       # Зависимости Python
├── .env                   # Переменные окружения
├── app/                   # Код приложения
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── services/
│   └── db/
├── alembic/              # Миграции БД
└── venv/                 # Виртуальное окружение
```

## 6. Устранение неполадок

### Проверка логов
```bash
# Логи Apache
tail -f /var/log/apache2/error.log

# Логи приложения (если используется systemd)
sudo journalctl -u fastapi -f
```

### Проверка соединения с БД
```bash
python test_connection.py
```

### Проверка прав доступа
```bash
chmod +x main.py
chmod 644 .htaccess
``` 