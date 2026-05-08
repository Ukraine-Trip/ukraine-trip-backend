import uuid
from sqlalchemy import Column, String, Float, Boolean, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Для фільтрації
    region = Column(String, index=True, nullable=False) # Наприклад: "Львівська", "Закарпатська"
    type = Column(String, index=True, nullable=False)   # Наприклад: "замок", "парк", "музей"
    
    rating = Column(Float, default=0.0)                 # Середній рейтинг
    
    # Координати для мапи
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    
    # Для модерації (за замовчуванням False, поки адмін не схвалить)
    is_approved = Column(Boolean, default=False)
    priority = Column(Integer, default=3, server_default="3", nullable=False)

    # ID користувача який створив локацію (nullable щоб не зламати існуючі записи)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)