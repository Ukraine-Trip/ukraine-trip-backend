import uuid
from sqlalchemy import Column, String, Text, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base

class Trip(Base):
    __tablename__ = "trips"  # <--- Виправлено тут

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    nodes = relationship(
        "TripNode",
        back_populates="trip",
        cascade="all, delete-orphan",
        order_by="TripNode.order_index"
    )

class TripNode(Base):
    __tablename__ = "trip_nodes"  # <--- Виправлено тут

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    order_index = Column(Integer, nullable=False)

    trip = relationship("Trip", back_populates="nodes")
    location = relationship("Location")  # ← додано