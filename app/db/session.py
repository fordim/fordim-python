from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем URL базы данных из переменной окружения или используем значение по умолчанию
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4"
)

# Временный вывод для отладки
print("FastAPI DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)  # echo=True для логов SQL запросов

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()