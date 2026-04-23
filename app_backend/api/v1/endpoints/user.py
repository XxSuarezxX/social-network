from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.user import UserService
from schemas.user import UserCreate, UserResponse
from core.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user : UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)

    existing_user = await user_service.get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "Correo ya registrado")
    
    new_user = await user_service.create_user(user)
    return new_user