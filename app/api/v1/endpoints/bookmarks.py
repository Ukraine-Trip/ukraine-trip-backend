from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.crud import crud_bookmark, crud_location
from app.api.deps import get_current_user
from app.schemas.bookmark import BookmarkResponse

router = APIRouter()

@router.post("/{location_id}", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def add_bookmark(
    location_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Запит доступний тільки для авторизованих!
):
    """Додати локацію в 'Хочу відвідати'"""
    
    # 1. Перевіряємо, чи існує така локація в базі
    location = crud_location.get_location(db, location_id=str(location_id))
    if not location:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")
    
    # 2. Додаємо до закладок
    bookmark = crud_bookmark.create_bookmark(
        db=db, 
        user_id=current_user.id, 
        location_id=location_id
    )
    
    return bookmark