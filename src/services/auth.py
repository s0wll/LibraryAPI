from datetime import datetime, timezone, timedelta
from typing import Any

from fastapi import Response
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel

from src.schemas.users import UserAdd, UserAddRequest
from src.config import settings
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> Any:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    
    async def register_user(self, data: UserAddRequest) -> None:
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, username=data.username, hashed_password=hashed_password)
        await self.db.users.add(new_user_data)
        await self.db.commit()

    async def login_user(self, data: UserAddRequest) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        access_token = self.create_access_token({"user_id": user.id})
        return access_token
    
    async def get_one_or_none_user(self, user_id: int) -> BaseModel | None | Any:
        return await self.db.users.get_one_or_none(id=user_id)
    
    async def logout_user(self, response: Response) -> None:
        response.delete_cookie("access_token")
