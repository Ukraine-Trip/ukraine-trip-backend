import uuid
from sqlalchemy import Column, String, Text, Date, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base

class Trip(Base):
    __tablename__ = "trips"

    # Головний ідентифікатор маршруту
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    
    # Зв'язок з користувачем (Integer, бо таблиця users використовує числові ID)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Зв'язок із точками маршруту. 
    # cascade="all, delete-orphan" гарантує, що при видаленні маршруту всі його точки теж зникнуть.
    nodes = relationship(
        "TripNode", 
        back_populates="trip", 
        cascade="all, delete-orphan", 
        order_by="TripNode.order_index"
    )


class TripNode(Base):
    __tablename__ = "trip_nodes"

    # Головний ідентифікатор самої точки
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # До якого маршруту належить ця точка
    trip_id = Column(UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    
    # Зв'язок з локацією (база пам'яток)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    
    # Порядковий номер точки в маршруті (0, 1, 2...)
    order_index = Column(Integer, nullable=False)

    # Зворотний зв'язок з маршрутом
    trip = relationship("Trip", back_populates="nodes")