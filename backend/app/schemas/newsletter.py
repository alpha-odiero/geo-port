from pydantic import BaseModel, EmailStr
from datetime import datetime

class NewsletterSubscribe(BaseModel):
    email: EmailStr

class NewsletterSubscriberResponse(BaseModel):
    id: int
    email: EmailStr
    subscribed_at: datetime

    model_config = {
        "from_attributes": True
    }
