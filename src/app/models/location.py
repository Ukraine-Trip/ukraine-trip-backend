from sqlalchemy import Column, String, Text, Float
from .base import Base

class Location(Base):
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    region = Column(String)  # Наприклад, "Львівська обл."
    lat = Column(Float)      # Широта
    lon = Column(Float)      # Довгота
    category = Column(String) # "Парк", "Музей", "Ресторан"