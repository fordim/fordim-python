#!/usr/bin/env python3
"""
Проверка существующих задач
"""

import pymysql

def check_existing_tasks():
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
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
            
            print(f"Найдено задач: {len(tasks)}")
            for task in tasks:
                print(f"ID: {task[0]}, Название: {task[1]}, Описание: {task[2]}, Завершено: {task[3]}, Создано: {task[4]}")
        
        connection.close()
        
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    check_existing_tasks() 