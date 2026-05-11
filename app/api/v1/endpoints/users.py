from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserUpdateResponse
from app.api.deps import get_current_user, get_db
from app.core.security import get_password_hash, create_access_token
from app.crud.crud_user import get_user_by_email

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    """Отримання даних свого профілю (потребує токена)"""
    return current_user

@router.put("/me", response_model=UserUpdateResponse)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Оновлення даних свого профілю"""

    if user_in.full_name is not None:
        current_user.full_name = user_in.full_name
    
    email_changed = False
    if user_in.email is not None and user_in.email != current_user.email:
        user = get_user_by_email(db, email=user_in.email)
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ця електронна пошта вже використовується іншим користувачем",
            )
        current_user.email = user_in.email
        email_changed = True
    
    if user_in.password is not None:
        current_user.hashed_password = get_password_hash(user_in.password)

    db.commit()
    db.refresh(current_user)

    response_data = {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }
    
    if email_changed:
        new_token = create_access_token(subject=current_user.email)
        response_data["access_token"] = new_token
        response_data["token_type"] = "bearer"

    return response_data