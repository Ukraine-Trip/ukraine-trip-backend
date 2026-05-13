from fastapi import APIRouter, Depends, status, HTTPException # 👈 Додано HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from uuid import UUID
from app.services.optimizer import get_optimal_order

from app.db.session import get_db
from app.models.user import User
from app.models.trip import Trip, TripNode
from app.crud import crud_trip
from app.schemas.trip import TripCreate, TripResponse, TripNodeUpdate, RouteBuildRequest
from app.api.deps import get_current_user, get_trip_and_check_owner
from app.models.location import Location

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

@router.post("/build", response_model=TripResponse)
def build_optimized_route(request: RouteBuildRequest, db: Session = Depends(get_db)):
    # 1. Дістаємо локації за списком ID
    query = select(Location).where(Location.id.in_(request.location_ids))
    locations_from_db = db.execute(query).scalars().all()
    
    if len(locations_from_db) != len(request.location_ids):
        raise HTTPException(status_code=404, detail="Деякі локації не знайдено")

    # Створюємо словник для швидкого доступу та зберігаємо порядок фронта
    loc_map = {loc.id: loc for loc in locations_from_db}
    ordered_locs = [loc_map[lid] for lid in request.location_ids]

    # 2. Оптимізуємо порядок через OSRM
    coords = [{"lat": l.lat, "lon": l.lon} for l in ordered_locs]
    optimal_indices = get_optimal_order(coords)

    # 3. Створюємо Trip
    new_trip = Trip(title=request.title, user_id=1) # user_id тимчасово 1
    db.add(new_trip)
    db.flush()

    # 4. Створюємо TripNodes в новому порядку
    for new_index, orig_index in enumerate(optimal_indices):
        loc = ordered_locs[orig_index]
        node = TripNode(
            trip_id=new_trip.id,
            location_id=loc.id,
            order_index=new_index
        )
        db.add(node)
        
    db.commit()
    
    return crud_trip.get_trip(db, trip_id=new_trip.id)    
@router.get("/{id}", response_model=TripResponse)
def read_trip(id: UUID, db: Session = Depends(get_db)):
    """Деталі маршруту з усіма точками (доступно всім)"""
    trip = crud_trip.get_trip(db, trip_id=id)
    if not trip:
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")
    return trip

@router.put("/{trip_id}/nodes", response_model=TripResponse)
def update_trip_nodes(
    nodes_in: List[TripNodeUpdate], 
    db: Session = Depends(get_db),
    trip: Trip = Depends(get_trip_and_check_owner) 
):
    """Оновлення списку точок (додавання/видалення локацій, зміна черговості)"""
    return crud_trip.update_trip_nodes(db, trip_id=trip.id, nodes_in=nodes_in)

@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    db: Session = Depends(get_db),
    trip: Trip = Depends(get_trip_and_check_owner)
):
    """Видалення маршруту"""
    crud_trip.delete_trip(db, trip_id=trip.id)
    return None   