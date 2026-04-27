from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class BookmarkResponse(BaseModel):
    id: UUID
    user_id: int
    location_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)