from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
#from app.db.session import get_db
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserResponse
from app.models.user import User

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