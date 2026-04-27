from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.models.trip import Trip, TripNode
from app.schemas.trip import TripCreate, TripNodeUpdate

def get_trip(db: Session, trip_id: str | UUID):
    return db.query(Trip).filter(Trip.id == trip_id).first()

def create_trip(db: Session, obj_in: TripCreate, user_id: UUID):
    db_obj = Trip(**obj_in.model_dump(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_trip_nodes(db: Session, trip_id: UUID, nodes_in: List[TripNodeUpdate]):
    """Оновлення списку точок: видаляємо старі, створюємо нові"""
    # 1. Видаляємо всі існуючі точки цього маршруту
    db.query(TripNode).filter(TripNode.trip_id == trip_id).delete()
    
    # 2. Додаємо нові точки з правильним порядком
    for node in nodes_in:
        new_node = TripNode(
            trip_id=trip_id,
            location_id=node.location_id,
            order_index=node.order_index
        )
        db.add(new_node)
        
    db.commit()
    return get_trip(db, trip_id)

def delete_trip(db: Session, trip_id: UUID):
    trip = get_trip(db, trip_id)
    if trip:
        db.delete(trip)
        db.commit()
    return trip