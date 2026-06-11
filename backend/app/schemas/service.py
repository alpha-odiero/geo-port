from pydantic import BaseModel, Field
from datetime import datetime

class ServiceBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
