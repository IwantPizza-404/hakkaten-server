from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True