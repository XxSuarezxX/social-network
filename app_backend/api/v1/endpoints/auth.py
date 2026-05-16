from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from services.user import UserService
from services.auth_service import AuthService
from schemas.userLogin import UserLogin


router = APIRouter(prefix="/auth", tags=["Auth"])

def get_auth_service(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    return AuthService(user_service)

@router.post("/")
async def login(data: UserLogin, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.login_auth(data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos")
    return user