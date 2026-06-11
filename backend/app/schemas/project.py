from pydantic import BaseModel, Field
from datetime import datetime

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    tag: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=5)
    image_url: str = Field(..., min_length=5, max_length=255)

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
