from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ShipmentBase(BaseModel):
    tracking_number: str = Field(..., min_length=4, max_length=50)
    customer_name: str = Field(..., min_length=2, max_length=100)
    status: str = Field(..., min_length=2, max_length=50)
    current_location: str = Field(..., min_length=2, max_length=100)
    expected_delivery: str = Field(..., min_length=2, max_length=100)

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    customer_name: Optional[str] = None
    status: Optional[str] = None
    current_location: Optional[str] = None
    expected_delivery: Optional[str] = None

class ShipmentResponse(ShipmentBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
