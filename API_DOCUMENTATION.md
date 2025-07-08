# API Документация - Fordim Python Backend

## Обзор проекта

Это Flask-приложение с REST API для управления задачами и подписками. Проект использует SQLAlchemy для работы с базой данных и Alembic для миграций.

**Базовый URL:** `http://localhost:5000`

## Структура API

### Основные эндпоинты

#### 1. Главная страница
```
GET /
```
**Ответ:**
```json
{
  "message": "Добро пожаловать в Flask приложение!",
  "features": [
    {
      "name": "task_tracker",
      "url": "/api/tasks",
      "page": "/tasks-page"
    },
    {
      "name": "schedule",
      "url": "/api/schedule"
    },
    {
      "name": "subscription",
      "url": "/api/subscription",
      "page": "/subscriptions-page"
    }
  ]
}
```

#### 2. Проверка здоровья
```
GET /health
```
**Ответ:**
```json
{
  "status": "ok",
  "message": "Приложение работает"
}
```

#### 3. Отладка маршрутов
```
GET /debug/routes
```
**Ответ:** Список всех доступных маршрутов в приложении

---

## API Подписок (`/api/subscription`)

### Модель данных

```typescript
interface Subscription {
  id: number;
  name: string;                    // Имя подписки
  amount: number;                  // Сумма в копейках/центах
  billing_time: string;           // Время списания (формат: "15:30")
  replenishment_time: string;     // Время пополнения (формат: "15:30")
  frequency: "month" | "year";    // Частота повторения
  source: string;                 // Откуда списывается
  status: "completed" | "progress"; // Статус подписки
  created_at: string;             // ISO формат даты
  updated_at: string;             // ISO формат даты
}
```

### Эндпоинты

#### 1. Получение списка подписок
```
GET /api/subscription
```

**Параметры запроса:**
- `status` (опционально): `"completed"` | `"progress"`
- `frequency` (опционально): `"month"` | `"year"`
- `soon` (опционально): `"true"` - показывает подписки, которые нужно оплатить в ближайший час

**Пример запроса:**
```
GET /api/subscription?status=progress&frequency=month&soon=true
```

**Ответ:**
```json
{
  "subscriptions": [
    {
      "id": 1,
      "name": "Netflix",
      "amount": 99900,
      "billing_time": "15:30",
      "replenishment_time": "15:30",
      "frequency": "month",
      "source": "Сбербанк",
      "status": "progress",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "message": "Список подписок (фильтры: статус: progress, частота: month, скоро платить)",
  "total_count": 1,
  "filters": {
    "status": "progress",
    "frequency": "month",
    "soon": "true"
  }
}
```

#### 2. Получение конкретной подписки
```
GET /api/subscription/{id}
```

**Ответ:**
```json
{
  "subscription": {
    "id": 1,
    "name": "Netflix",
    "amount": 99900,
    "billing_time": "15:30",
    "replenishment_time": "15:30",
    "frequency": "month",
    "source": "Сбербанк",
    "status": "progress",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  },
  "message": "Подписка найдена"
}
```

#### 3. Создание подписки
```
POST /api/subscription
```

**Тело запроса:**
```json
{
  "name": "Netflix",
  "amount": 99900,
  "billing_time": "15:30",
  "replenishment_time": "15:30",
  "frequency": "month",
  "source": "Сбербанк",
  "status": "progress"
}
```

**Обязательные поля:** `name`, `amount`, `billing_time`, `replenishment_time`, `frequency`, `source`

**Ответ (201):**
```json
{
  "message": "Подписка создана",
  "subscription": {
    "id": 1,
    "name": "Netflix",
    "amount": 99900,
    "billing_time": "15:30",
    "replenishment_time": "15:30",
    "frequency": "month",
    "source": "Сбербанк",
    "status": "progress",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 4. Обновление подписки
```
PUT /api/subscription/{id}
```

**Тело запроса (все поля опциональны):**
```json
{
  "name": "Netflix Premium",
  "amount": 129900,
  "billing_time": "16:00",
  "replenishment_time": "16:00",
  "frequency": "month",
  "source": "Тинькофф",
  "status": "completed"
}
```

**Ответ:**
```json
{
  "success": true,
  "message": "Подписка обновлена",
  "subscription": {
    "id": 1,
    "name": "Netflix Premium",
    "amount": 129900,
    "billing_time": "16:00",
    "replenishment_time": "16:00",
    "frequency": "month",
    "source": "Тинькофф",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

#### 5. Завершение подписки
```
POST /api/subscription/{id}/complete
```

**Ответ:**
```json
{
  "message": "Подписка завершена",
  "subscription": {
    "id": 1,
    "name": "Netflix",
    "amount": 99900,
    "billing_time": "15:30",
    "replenishment_time": "15:30",
    "frequency": "month",
    "source": "Сбербанк",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

#### 6. Удаление подписки
```
DELETE /api/subscription/{id}
```

**Ответ:**
```json
{
  "message": "Подписка удалена"
}
```

---

## API Задач (`/api/tasks`)

### Модель данных

```typescript
interface Task {
  id: number;
  title: string;                   // Заголовок задачи
  description: string | null;      // Описание задачи
  status: "completed" | "pending"; // Статус задачи
  created_at: string;              // ISO формат даты
  updated_at: string;              // ISO формат даты
}
```

### Эндпоинты

#### 1. Получение списка задач
```
GET /api/tasks
```

**Ответ:**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Изучить Angular",
      "description": "Изучить основы Angular для фронтенда",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ],
  "message": "Список задач"
}
```

#### 2. Создание задачи
```
POST /api/tasks
```

**Тело запроса:**
```json
{
  "title": "Изучить Angular",
  "description": "Изучить основы Angular для фронтенда",
  "status": "pending"
}
```

**Ответ:**
```json
{
  "message": "Задача создана",
  "task": {
    "id": 1,
    "title": "Изучить Angular",
    "description": "Изучить основы Angular для фронтенда",
    "status": "pending",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### 3. Обновление задачи
```
PUT /api/tasks/{id}
```

**Тело запроса (все поля опциональны):**
```json
{
  "title": "Изучить Angular (обновлено)",
  "description": "Изучить основы Angular для фронтенда - в процессе",
  "status": "completed"
}
```

**Ответ:**
```json
{
  "message": "Задача обновлена",
  "task": {
    "id": 1,
    "title": "Изучить Angular (обновлено)",
    "description": "Изучить основы Angular для фронтенда - в процессе",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

#### 4. Удаление задачи
```
DELETE /api/tasks/{id}
```

**Ответ:**
```json
{
  "message": "Задача удалена"
}
```

---

## Коды ошибок

### HTTP статусы
- `200` - Успешный запрос
- `201` - Ресурс создан
- `400` - Ошибка валидации данных
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера

### Примеры ошибок

**Ошибка валидации:**
```json
{
  "error": "frequency должен быть 'month' или 'year'"
}
```

**Ресурс не найден:**
```json
{
  "error": "Подписка не найдена"
}
```

---

## Структура базы данных

### Таблица `subscriptions`
```sql
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
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
```

### Таблица `tasks`
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    is_completed INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Рекомендации для Angular

### 1. Создание сервисов

```typescript
// subscription.service.ts
@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private apiUrl = 'http://localhost:5000/api/subscription';

  constructor(private http: HttpClient) {}

  getSubscriptions(filters?: any): Observable<any> {
    return this.http.get(this.apiUrl, { params: filters });
  }

  createSubscription(subscription: any): Observable<any> {
    return this.http.post(this.apiUrl, subscription);
  }

  updateSubscription(id: number, subscription: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, subscription);
  }

  deleteSubscription(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }

  completeSubscription(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/complete`, {});
  }
}
```

### 2. Интерфейсы TypeScript

```typescript
// models/subscription.interface.ts
export interface Subscription {
  id: number;
  name: string;
  amount: number;
  billing_time: string;
  replenishment_time: string;
  frequency: 'month' | 'year';
  source: string;
  status: 'completed' | 'progress';
  created_at: string;
  updated_at: string;
}

// models/task.interface.ts
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: 'completed' | 'pending';
  created_at: string;
  updated_at: string;
}
```

### 3. Обработка ошибок

```typescript
// error.interceptor.ts
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 400) {
          // Обработка ошибок валидации
          console.error('Ошибка валидации:', error.error.error);
        } else if (error.status === 404) {
          // Ресурс не найден
          console.error('Ресурс не найден');
        }
        return throwError(() => error);
      })
    );
  }
}
```

---

## Запуск проекта

1. **Установка зависимостей:**
```bash
pip install -r requirements.txt
```

2. **Настройка базы данных:**
```bash
alembic upgrade head
```

3. **Запуск сервера:**
```bash
python run.py
```

Сервер будет доступен по адресу: `http://localhost:5000`

---

## Дополнительные возможности

- **Фильтрация подписок:** По статусу, частоте, времени оплаты
- **Валидация данных:** Автоматическая проверка входных данных
- **Логирование:** Все операции логируются
- **Миграции:** Использование Alembic для управления схемой БД

Эта документация содержит всю необходимую информацию для интеграции с Angular фронтендом! 