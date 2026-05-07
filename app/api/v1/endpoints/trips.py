from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.user import User
from app.models.trip import Trip
from app.crud import crud_trip
from app.schemas.trip import TripCreate, TripResponse, TripNodeUpdate
from app.api.deps import get_current_user, get_trip_and_check_owner

router = APIRouter()

@router.get("/", response_model=List[TripResponse])
def read_all_trips(db: Session = Depends(get_db)):
    """Список усіх маршрутів (публічно)"""
    return crud_trip.get_all_trips(db)

@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Захищено токеном
):
    """Створення нового маршруту (назва, опис, дати)"""
    return crud_trip.create_trip(db, obj_in=trip_in, user_id=current_user.id)

@router.get("/{id}", response_model=TripResponse)
def read_trip(id: UUID, db: Session = Depends(get_db)):
    """Деталі маршруту з усіма точками (доступно всім)"""
    trip = crud_trip.get_trip(db, trip_id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")
    return trip

@router.put("/{trip_id}/nodes", response_model=TripResponse)
def update_trip_nodes(
    nodes_in: List[TripNodeUpdate], # Приймаємо масив точок
    db: Session = Depends(get_db),
    # Захист: пустить тільки власника маршруту
    trip: Trip = Depends(get_trip_and_check_owner) 
):
    """Оновлення списку точок (додавання/видалення локацій, зміна черговості)"""
    return crud_trip.update_trip_nodes(db, trip_id=trip.id, nodes_in=nodes_in)

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    db: Session = Depends(get_db),
    # Захист: пустить тільки власника маршруту
    trip: Trip = Depends(get_trip_and_check_owner)
):
    """Видалення маршруту"""
    crud_trip.delete_trip(db, trip_id=trip.id)
    return None