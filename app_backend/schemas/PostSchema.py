from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class PostSchema(BaseModel):
    content : str = Field(..., min_length=1, max_length=500)

class AuthorPost(BaseModel):
    username : str

    class Config:
        from_attributes = True

class PostResponse(BaseModel):
    id : UUID
    content: str
    created_at : datetime
    author : AuthorPost

    class Config:
        from_attributes = True

class PostToUpdate(BaseModel):
    id : UUID
    content : str = Field(..., min_length=1, max_length=200)

