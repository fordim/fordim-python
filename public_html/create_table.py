#!/usr/bin/env python3
"""
Создание таблицы tasks
"""

import pymysql

def create_tasks_table():
    try:
        connection = pymysql.connect(
            host="141.8.192.169",
            port=3306,
            user="a0739858_fordim",
            password="HtPs84Xrt@wTaK",
            database="a0739858_fordim_web",
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Создаем таблицу tasks
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            cursor.execute(create_table_sql)
            connection.commit()
            
            print("✅ Таблица tasks создана успешно!")
            
            # Проверяем структуру
            cursor.execute("DESCRIBE tasks")
            columns = cursor.fetchall()
            print("Структура таблицы tasks:")
            for col in columns:
                print(f"  {col[0]} - {col[1]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка создания таблицы: {e}")
        return False

if __name__ == "__main__":
    create_tasks_table() 