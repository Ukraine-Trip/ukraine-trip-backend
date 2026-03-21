from fastapi import APIRouter

router = APIRouter()

# TODO для розробника (Auth):
# 1. Створити Pydantic-схеми UserCreate та UserResponse в папці schemas/user.py
# 2. Реалізувати хешування паролів через бібліотеку passlib
# 3. Налаштувати генерацію JWT токенів

@router.post("/register")
async def register_user():
    """Ендпоінт для реєстрації нового користувача"""
    return {"message": "Тут буде логіка реєстрації. Поки що це заглушка."}

@router.post("/login")
async def login_user():
    """Ендпоінт для логіну та отримання токена"""
    return {"access_token": "fake-jwt-token", "token_type": "bearer"}