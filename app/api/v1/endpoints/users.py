from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.api.deps import get_current_user, get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """Отримання даних свого профілю (потребує токена)"""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Оновлення даних свого профілю"""

    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)

    db.commit()
    db.refresh(current_user)

    return current_user