from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# URL підключення
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@ukraine_trip_db:5432/ukraine_trip")

# Створення рушія (Зверни увагу: create_engine, а НЕ create_async_engine)
engine = create_engine(DATABASE_URL)

# Створення сесії (Зверни увагу: sessionmaker, а не AsyncSession)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()