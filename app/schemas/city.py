from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CityResponse(BaseModel):
    id: UUID
    name: str
    region: str
    lat: float = 0.0
    lng: float = 0.0

    model_config = ConfigDict(from_attributes=True)