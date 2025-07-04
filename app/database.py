from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Путь к .env файлу (на уровень выше app/)
env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

# Загружаем переменные окружения из .env файла
load_dotenv(env_file)

# Получаем URL базы данных из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL не найден в переменных окружения. Проверьте файл .env")

# Создаем движок
engine = create_engine(DATABASE_URL, echo=True)

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 