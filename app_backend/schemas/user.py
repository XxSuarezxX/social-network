from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email : EmailStr
    username : str
    password: str

class UserResponse(BaseModel):
    id : UUID
    email : str
    username : str
    