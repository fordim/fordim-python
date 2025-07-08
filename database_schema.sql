-- Схема базы данных для проекта Fordim Python Backend
-- Экспорт для использования в Angular проекте

-- Таблица подписок
CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    amount INTEGER NOT NULL,
    billing_time VARCHAR(50) NOT NULL,
    replenishment_time VARCHAR(50) NOT NULL,
    frequency VARCHAR(10) NOT NULL CHECK (frequency IN ('month', 'year')),
    source VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'progress' CHECK (status IN ('completed', 'progress')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Таблица задач
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_completed INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_subscriptions_frequency ON subscriptions(frequency);
CREATE INDEX IF NOT EXISTS idx_subscriptions_billing_time ON subscriptions(billing_time);
CREATE INDEX IF NOT EXISTS idx_tasks_is_completed ON tasks(is_completed);

-- Примеры данных для тестирования

-- Подписки
INSERT INTO subscriptions (name, amount, billing_time, replenishment_time, frequency, source, status) VALUES
('Netflix', 99900, '15:30', '15:30', 'month', 'Сбербанк', 'progress'),
('Spotify', 29900, '10:00', '10:00', 'month', 'Тинькофф', 'progress'),
('YouTube Premium', 39900, '20:15', '20:15', 'month', 'Сбербанк', 'completed'),
('Adobe Creative Cloud', 299900, '12:00', '12:00', 'year', 'Тинькофф', 'progress'),
('GitHub Pro', 49900, '09:30', '09:30', 'month', 'Сбербанк', 'progress');

-- Задачи
INSERT INTO tasks (title, description, is_completed) VALUES
('Изучить Angular', 'Изучить основы Angular для фронтенда', 0),
('Создать API документацию', 'Создать подробную документацию для API', 1),
('Настроить CORS', 'Настроить CORS для работы с Angular', 0),
('Добавить валидацию', 'Добавить валидацию входных данных', 1),
('Оптимизировать запросы', 'Оптимизировать SQL запросы', 0);

-- Комментарии к полям

/*
ПОЛЯ ТАБЛИЦЫ SUBSCRIPTIONS:
- id: Уникальный идентификатор подписки
- name: Название подписки (например: "Netflix", "Spotify")
- amount: Сумма в копейках/центах (99900 = 999 рублей)
- billing_time: Время списания в формате "HH:MM" (например: "15:30")
- replenishment_time: Время пополнения в формате "HH:MM"
- frequency: Частота повторения ("month" или "year")
- source: Источник списания (например: "Сбербанк", "Тинькофф")
- status: Статус подписки ("progress" - активна, "completed" - завершена)
- created_at: Дата и время создания записи
- updated_at: Дата и время последнего обновления

ПОЛЯ ТАБЛИЦЫ TASKS:
- id: Уникальный идентификатор задачи
- title: Заголовок задачи
- description: Подробное описание задачи (может быть NULL)
- is_completed: Статус выполнения (0 - не выполнено, 1 - выполнено)
- created_at: Дата и время создания записи
- updated_at: Дата и время последнего обновления

ВАЖНЫЕ ЗАМЕЧАНИЯ:
1. Суммы хранятся в копейках/центах для избежания проблем с плавающей точкой
2. Время хранится в строковом формате "HH:MM" для простоты
3. Статус задач хранится как INTEGER (0/1) в БД, но API возвращает строки ("pending"/"completed")
4. Все даты хранятся в UTC формате
*/ 