from sqlalchemy import Column, String, ForeignKey, JSON, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Trip(Base):
    title = Column(String)
    user_id = Column(Integer, ForeignKey("user.id")) # Тепер Integer імпортовано!
    route_data = Column(JSON)
    
    user = relationship("User")