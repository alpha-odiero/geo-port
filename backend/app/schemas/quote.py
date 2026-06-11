from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class QuoteBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    service: str = Field(..., min_length=2, max_length=100)
    cargo_weight: float = Field(..., gt=0)

class QuoteCreate(QuoteBase):
    pass

class QuoteResponse(QuoteBase):
    id: int
    tracking_number: str | None = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
