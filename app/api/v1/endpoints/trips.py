from fastapi import APIRouter, Depends, status, HTTPException, Query # 👈 Додано HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional
from uuid import UUID
from app.services.optimizer import get_optimal_order

from app.db.session import get_db
from app.models.user import User
from app.models.trip import Trip, TripNode
from app.crud import crud_trip
from app.schemas.trip import TripCreate, TripResponse, TripNodeUpdate, RouteBuildRequest, RouteOptimizeRequest, RouteOptimizeResponse
from app.api.deps import get_current_user, get_trip_and_check_owner, get_current_user_optional
from app.models.location import Location

router = APIRouter()

@router.get("/", response_model=List[TripResponse])
def read_all_trips(
    filter_type: str = Query("all", description="Фільтр маршрутів: 'all', 'my', 'system'"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Список маршрутів з фільтрацією (публічно або за власником)"""
    if filter_type == "my":
        if not current_user:
            raise HTTPException(status_code=401, detail="Авторизуйтесь для перегляду власних маршрутів")
        return crud_trip.get_all_trips(db, user_id=current_user.id)
    elif filter_type == "system":
        return crud_trip.get_all_trips(db, is_system=True)
    
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
    """Побудова маршруту: автоматична оптимізація (OSRM) або збереження порядку користувача"""
    
    # 1. Дістаємо локації за списком ID
    query = select(Location).where(Location.id.in_(request.location_ids))
    locations_from_db = db.execute(query).scalars().all()
    
    if len(locations_from_db) != len(request.location_ids):
        raise HTTPException(status_code=404, detail="Деякі локації не знайдено в базі")

    # Створюємо словник для швидкого доступу та зберігаємо початковий порядок фронтенду
    loc_map = {loc.id: loc for loc in locations_from_db}
    ordered_locs = [loc_map[lid] for lid in request.location_ids]

    # 2. Перевіряємо, чи потрібна оптимізація (прапорець optimize)
    if request.optimize:
        # Звертаємось до OSRM для розрахунку найкоротшого шляху
        coords = [{"lat": l.lat, "lon": l.lon} for l in ordered_locs]
        final_indices = get_optimal_order(coords)
    else:
        # Якщо юзер хоче свій порядок, просто створюємо послідовність [0, 1, 2, 3...]
        final_indices = list(range(len(ordered_locs)))

    # 3. Створюємо сам маршрут (Trip)
    # TODO: Замінити user_id=1 на реального користувача (current_user.id), коли підключиш авторизацію для цього роуту
    new_trip = Trip(title=request.title, user_id=1) 
    db.add(new_trip)
    db.flush() # flush генерує new_trip.id, який нам потрібен для TripNode

    # 4. Створюємо точки маршруту (TripNodes) у фінальному порядку
    for new_index, orig_index in enumerate(final_indices):
        loc = ordered_locs[orig_index]
        node = TripNode(
            trip_id=new_trip.id,
            location_id=loc.id,
            order_index=new_index # 0, 1, 2...
        )
        db.add(node)
        
    db.commit()

    # Повертаємо готовий маршрут з усією вкладеністю (через selectinload)
    return crud_trip.get_trip(db, trip_id=new_trip.id)

@router.post("/optimize", response_model=RouteOptimizeResponse)
def optimize_route_order(request: RouteOptimizeRequest):
    """Повертає оптимальний порядок індексів через OSRM (без збереження в БД)"""
    ordered_indices = get_optimal_order(request.coordinates)
    return RouteOptimizeResponse(ordered_indices=ordered_indices)

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