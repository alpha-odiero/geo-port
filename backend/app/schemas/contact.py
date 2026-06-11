from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ContactMessageBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=1000)

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageResponse(ContactMessageBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
