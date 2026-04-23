from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate
from schemas.userLogin import UserLogin
from core.security import get_password_hash, verify_password

class UserService:

    def __init__(self, db):
        self.db = db

    async def get_user_by_email(self, email: str):
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_user(self, user: UserCreate):
        hashed_pw = get_password_hash(user.password)

        new_user = User(
            email = user.email,
            username = user.username,
            hashed_password = hashed_pw)

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def user_login(self, user: UserLogin):
        user_db = await self.get_user_by_email(user.email)

        if user_db and verify_password(user.password, user_db.hashed_password):
            return user_db
        return None
