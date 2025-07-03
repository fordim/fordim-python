from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://a0739858_fordim:HtPs84Xrt%40wTaK@141.8.192.169:3306/a0739858_fordim_web?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Connection successful, query result:", result.scalar())
    except Exception as e:
        print("Connection failed:", e)

if __name__ == "__main__":
    test_connection()