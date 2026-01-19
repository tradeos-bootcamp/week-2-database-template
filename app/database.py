from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Используем переменную окружения или значение по умолчанию
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://tradeos_user:tradeos_password@localhost:5432/tradeos_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Функция для получения сессии БД (будет использоваться в Dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
