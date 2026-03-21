from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Імпортуємо маршрути (ендпоінти) з нашої структури
from src.app.api.v1 import auth, trips, ai

app = FastAPI(
    title="Ukraine Trip API",
    description="Бекенд для генерації смарт-маршрутів по Україні",
    version="1.0.0"
)

# Дозволяємо фронтенду підключатися без помилок CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо роутери і розбиваємо їх по категоріях для Swagger
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Авторизація (Шемік)"])
app.include_router(trips.router, prefix="/api/v1/trips", tags=["Маршрути (Артік)"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ШІ Асистент (Назік Мик)"])

@app.get("/healthcheck", tags=["Система"])
def healthcheck():
    return {"status": "success", "message": "Архітектура успішно розгорнута!"}