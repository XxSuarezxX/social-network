from services.user import UserService
from core.security import create_access_token, verify_password
from schemas.userLogin import UserLogin


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login_auth(self, user: UserLogin):
        user_db = await self.user_service.get_user_by_email(user.email)

        if user_db and verify_password(user.password, user_db.hashed_password):
            token = await create_access_token(str(user_db.id))
            return {"access_token": token, "token_type": "bearer"}
        return None
