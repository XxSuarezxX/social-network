import bcrypt
import secrets
import datetime
import jwt
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from core.security import settings
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db

security_scheme = HTTPBearer()


def get_password_hash(password: str) -> str:
    encoded_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(encoded_password, salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> str:
    encoded_password = password.encode('utf-8')
    encoded_hash = hashed_password.encode('utf-8')
    return bcrypt.checkpw(encoded_password, encoded_hash)


async def create_random_token(length=32):
    return secrets.token_urlsafe(length)

async def create_access_token(user_uuid):
    payload = {"sub": user_uuid,
               "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.access_token_expire)}
    return jwt.encode(payload, settings.secret_key, algorithm= settings.algorithm)


oauth2_scheme =OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token = Depends(security_scheme), 
    db: AsyncSession = Depends(get_db)):
    from services.user import UserService

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},)
    
    try:
        token_data = token.credentials 
        payload = jwt.decode(
            token_data, 
            settings.secret_key, 
            algorithms=[settings.algorithm])
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except (JWTError, AttributeError):
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    
    if user is None:
        raise credentials_exception
        
    return user 