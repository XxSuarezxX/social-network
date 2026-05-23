from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password: str

class UserResponse(BaseModel):
    id : UUID
    email : EmailStr
    username : str
    full_name: str | None = None
    bio: str | None = None
    profile_picture: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: str | None = None
    bio: str | None = None
    profile_picture: str | None = None
