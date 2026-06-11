from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    current_location = Column(String(100), nullable=False)
    expected_delivery = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
