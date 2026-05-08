from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.crud import crud_location
from app.schemas.location import LocationCreate, LocationResponse, ReviewCreate
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/my", response_model=List[LocationResponse])
def read_my_locations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # обов'язкова авторизація
):
    return crud_location.get_my_locations(db, owner_id=current_user.id)

@router.get("/", response_model=List[LocationResponse])
def read_locations(
    region: str = Query(None, description="Фільтр за областю"),
    type: str = Query(None, description="Фільтр за типом (наприклад: замок, парк)"),
    min_rating: float = Query(None, description="Мінімальний рейтинг"),
    db: Session = Depends(get_db)
):
    """Отримання списку локацій (з фільтрами)"""
    return crud_location.get_locations(db, region=region, loc_type=type, min_rating=min_rating)

@router.get("/{id}", response_model=LocationResponse)
def read_location(id: UUID, db: Session = Depends(get_db)):
    """Детальна інформація про конкретне місце"""
    location = crud_location.get_location(db, location_id=str(id))
    if not location:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")
    return location

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location_in: LocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Вимагаємо токен!
):
    """Додавання нової локації (за замовчуванням is_approved=False)"""
    return crud_location.create_location(db, obj_in=location_in, owner_id=current_user.id)

@router.post("/{id}/reviews")
def add_review(
    id: UUID,
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Вимагаємо токен!
):
    """Залишити відгук або оцінку місцю"""
    location = crud_location.get_location(db, location_id=str(id))
    if not location:
        raise HTTPException(status_code=404, detail="Локацію не знайдено")
    
    # ТИМЧАСОВА ЗАГЛУШКА: Поки що просто повертаємо успіх. 
    # Повноцінне збереження зробимо, коли створимо таблицю Review.
    return {
        "message": f"Відгук для '{location.name}' успішно додано!", 
        "rating": review_in.rating,
        "user_email": current_user.email
    }


@router.get("/", response_model=List[LocationResponse])
def read_locations(
    region: str = Query(None, description="Фільтр за областю"),
    type: str = Query(None, description="Фільтр за типом"),
    min_rating: float = Query(None, description="Мінімальний рейтинг"),
    
    # ДОДАЛИ параметр зуму
    zoom: int = Query(None, description="Зум карти (1-20) для фільтрації маркерів LOD"), 
    
    db: Session = Depends(get_db)
):
    """Отримання списку локацій (з фільтрами)"""
    return crud_location.get_locations(
        db, 
        region=region, 
        loc_type=type, 
        min_rating=min_rating, 
        zoom=zoom # Передаємо зум у базу
    )