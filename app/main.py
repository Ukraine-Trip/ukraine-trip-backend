from fastapi import FastAPI
from app.api.v1.api import api_router
from app.api.v1 import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Ukraine Trip API",
    description="Сервіс для створення туристичних маршрутів Україною 🗺️",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Ukraine Trip API!",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "healthy"}