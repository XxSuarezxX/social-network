import bcrypt
import secrets
import datetime
import jwt
from core.config import settings

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