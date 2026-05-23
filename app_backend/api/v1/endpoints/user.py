from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.user import UserService
from schemas.user import UserCreate, UserResponse
from core.database import get_db
from core.security import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def register(user : UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)

    existing_user = await user_service.get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "Correo ya registrado")
    
    new_user = await user_service.create_user(user)
    return new_user

@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: str = Depends(get_current_user)):

    return current_user
        