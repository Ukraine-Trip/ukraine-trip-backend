import os

class Settings:
    PROJECT_NAME: str = "Ukraine Trip API"
    
    
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

settings = Settings()