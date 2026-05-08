from sqlalchemy.orm import Session
from uuid import UUID

from app.models.location import Location
from app.schemas.location import LocationCreate

def get_locations(
    db: Session, 
    region: str = None, 
    loc_type: str = None, 
    min_rating: float = None, 
    zoom: int = None
):
    """Отримання списку локацій з фільтрами та LOD (Level of Detail)"""
    
    # Завжди показуємо тільки схвалені модератором локації
    query = db.query(Location).filter(Location.is_approved == True)
    
    # --- 1. Базові фільтри ---
    if region:
        query = query.filter(Location.region == region)
    if loc_type:
        query = query.filter(Location.type == loc_type)
    if min_rating:
        query = query.filter(Location.rating >= min_rating)
        
    # --- 2. Логіка LOD (Фільтрація за зумом) ---
    if zoom is not None:
        if zoom <= 7:
            # Zoom 1-7: Тільки найважливіші точки (пріоритет 1 - обласні центри)
            query = query.filter(Location.priority == 1)
        elif 8 <= zoom <= 11:
            # Zoom 8-11: Середні та великі точки (пріоритети 1, 2, 3 - замки, музеї)
            query = query.filter(Location.priority <= 3)
        # Якщо zoom >= 12, додаткові фільтри не застосовуються 
        # (база віддасть абсолютно всі точки, включаючи дрібні кафе та АЗС)
        
    return query.all()


def get_location(db: Session, location_id: str | UUID):
    """Отримання детальної інформації про конкретну локацію за її ID"""
    return db.query(Location).filter(Location.id == location_id).first()


def create_location(db: Session, obj_in: LocationCreate):
    """Створення нової локації"""
    
    # model_dump() акуратно перетворює Pydantic-схему на словник для бази
    db_obj = Location(**obj_in.model_dump())
    
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    return db_obj

# ТИМЧАСОВА ЗАГЛУШКА ДЛЯ ВІДГУКІВ
# Коли у нас з'явиться таблиця Reviews, ми додамо сюди функцію create_review