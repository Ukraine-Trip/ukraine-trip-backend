import os

class Settings:
    PROJECT_NAME: str = "Ukraine Trip API"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-for-dev")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+asyncpg://user:password@db:5432/ukraine_trip"
    )
    
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# ОЦЕЙ РЯДОК НАЙГОЛОВНІШИЙ
settings = Settings()