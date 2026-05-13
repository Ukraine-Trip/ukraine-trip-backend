from sqlalchemy import Column, Integer, String
from app.db.session import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    region = Column(String, nullable=False, index=True)