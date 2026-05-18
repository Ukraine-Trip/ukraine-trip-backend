from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from datetime import date
from uuid import UUID
from app.schemas.location import LocationResponse

class TripCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class TripNodeUpdate(BaseModel):
    location_id: UUID
    order_index: int

class TripNodeResponse(BaseModel):
    id: UUID
    location_id: UUID
    order_index: int
    location: Optional[LocationResponse] = None 
    model_config = ConfigDict(from_attributes=True)

class TripResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    nodes: List[TripNodeResponse] = Field(default=[], alias="trip_nodes")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class RouteBuildRequest(BaseModel):
    title: str
    location_ids: List[UUID]
    optimize: bool = True
