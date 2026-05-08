from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from uuid import UUID

class LocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    region: str
    type: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    priority: int = 3

class LocationCreate(LocationBase):
    pass

class LocationResponse(LocationBase):
    id: UUID
    rating: float
    is_approved: bool

    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# Схема для 4-го ендпоінту (відгуки)
class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Оцінка від 1 до 5")
    comment: Optional[str] = None
