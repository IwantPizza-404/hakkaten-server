from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PostBase(BaseModel):
    content: str

    class Config:
        from_attributes = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    image_url: Optional[str] = Field(default=None)
