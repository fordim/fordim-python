# Интеграция с Angular - Краткое руководство

## Основные настройки

### 1. Базовый URL API
```typescript
export const API_BASE_URL = 'http://localhost:5000';
```

### 2. Эндпоинты
```typescript
export const API_ENDPOINTS = {
  SUBSCRIPTIONS: '/api/subscription',
  TASKS: '/api/tasks',
  HEALTH: '/health'
};
```

### 3. Типы данных
```typescript
// Статусы подписок
export type SubscriptionStatus = 'completed' | 'progress';

// Частота подписок
export type SubscriptionFrequency = 'month' | 'year';

// Статусы задач
export type TaskStatus = 'completed' | 'pending';
```

### 4. Настройка CORS (если нужно)
В вашем Flask приложении может потребоваться добавить CORS:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешить все домены для разработки
```

### 5. Основные сервисы Angular

#### SubscriptionService
```typescript
@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private apiUrl = `${API_BASE_URL}${API_ENDPOINTS.SUBSCRIPTIONS}`;

  constructor(private http: HttpClient) {}

  // Получить все подписки
  getSubscriptions(filters?: any): Observable<any> {
    return this.http.get(this.apiUrl, { params: filters });
  }

  // Создать подписку
  createSubscription(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  // Обновить подписку
  updateSubscription(id: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }

  // Завершить подписку
  completeSubscription(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${id}/complete`, {});
  }

  // Удалить подписку
  deleteSubscription(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
```

#### TaskService
```typescript
@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private apiUrl = `${API_BASE_URL}${API_ENDPOINTS.TASKS}`;

  constructor(private http: HttpClient) {}

  // Получить все задачи
  getTasks(): Observable<any> {
    return this.http.get(this.apiUrl);
  }

  // Создать задачу
  createTask(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  // Обновить задачу
  updateTask(id: number, data: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, data);
  }

  // Удалить задачу
  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
```

### 6. Интерфейсы TypeScript

```typescript
// subscription.interface.ts
export interface Subscription {
  id: number;
  name: string;
  amount: number;
  billing_time: string;
  replenishment_time: string;
  frequency: SubscriptionFrequency;
  source: string;
  status: SubscriptionStatus;
  created_at: string;
  updated_at: string;
}

// task.interface.ts
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

// API ответы
export interface ApiResponse<T> {
  message: string;
  [key: string]: any;
}

export interface SubscriptionsResponse extends ApiResponse<Subscription[]> {
  subscriptions: Subscription[];
  total_count: number;
  filters?: any;
}
```

### 7. Утилиты для работы с данными

```typescript
// utils/currency.util.ts
export class CurrencyUtil {
  // Конвертировать копейки в рубли
  static kopeksToRubles(kopeks: number): number {
    return kopeks / 100;
  }

  // Конвертировать рубли в копейки
  static rublesToKopeks(rubles: number): number {
    return Math.round(rubles * 100);
  }

  // Форматировать сумму для отображения
  static formatCurrency(amount: number): string {
    return new Intl.NumberFormat('ru-RU', {
      style: 'currency',
      currency: 'RUB'
    }).format(amount);
  }
}

// utils/time.util.ts
export class TimeUtil {
  // Форматировать время из "HH:MM" в читаемый вид
  static formatTime(time: string): string {
    return time; // Можно добавить дополнительное форматирование
  }

  // Проверить, скоро ли нужно платить (в ближайший час)
  static isPaymentSoon(billingTime: string): boolean {
    const now = new Date();
    const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
    
    // Простая проверка - можно улучшить
    return billingTime === currentTime;
  }
}
```

### 8. Обработка ошибок

```typescript
// interceptors/error.interceptor.ts
@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = 'Произошла ошибка';
        
        if (error.error && error.error.error) {
          errorMessage = error.error.error;
        } else if (error.status === 404) {
          errorMessage = 'Ресурс не найден';
        } else if (error.status === 400) {
          errorMessage = 'Ошибка валидации данных';
        }
        
        // Показать уведомление пользователю
        console.error('API Error:', errorMessage);
        
        return throwError(() => error);
      })
    );
  }
}
```

### 9. Настройка в app.module.ts

```typescript
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ErrorInterceptor } from './interceptors/error.interceptor';

@NgModule({
  imports: [
    HttpClientModule,
    // ... другие импорты
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true
    }
  ],
  // ... остальная конфигурация
})
export class AppModule { }
```

## Быстрый старт

1. Скопируйте файлы `API_DOCUMENTATION.md`, `database_schema.sql` и `ANGULAR_INTEGRATION.md` в ваш Angular проект
2. Создайте сервисы и интерфейсы по образцам выше
3. Настройте обработку ошибок
4. Запустите Flask backend: `python run.py`
5. Запустите Angular: `ng serve`

## Полезные команды для тестирования

```bash
# Проверить здоровье API
curl http://localhost:5000/health

# Получить список подписок
curl http://localhost:5000/api/subscription

# Создать подписку
curl -X POST http://localhost:5000/api/subscription \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","amount":99900,"billing_time":"15:30","replenishment_time":"15:30","frequency":"month","source":"Test"}'
``` 