from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date
from uuid import UUID

# Дані для створення маршруту
class TripCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

# Дані для оновлення списку точок (PUT /trips/{id}/nodes)
class TripNodeUpdate(BaseModel):
    location_id: UUID
    order_index: int

# Відповідь з точкою
class TripNodeResponse(BaseModel):
    id: UUID
    location_id: UUID
    order_index: int
    model_config = ConfigDict(from_attributes=True)

# Відповідь з усім маршрутом (включаючи список точок)
class TripResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    user_id: UUID
    nodes: List[TripNodeResponse] = [] # Вкладений список точок

    model_config = ConfigDict(from_attributes=True)