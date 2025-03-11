from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.schemas.users import User
from src.services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        int | None, Query(None, ge=1, lt=30, description="Количество отелей на одной странице")
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


# UserIdDep = Annotated[int, Depends(get_current_user_id)]  # Пока не нужно


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


async def get_current_user(db: DBDep, token: str = Depends(get_token)) -> User:
    user_id = get_current_user_id(token)
    user = await AuthService(db).get_one_or_none_user(user_id=user_id)
    return user


UserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="У вас недостаточно прав")
    return current_user


AdminDep = Annotated[User, Depends(get_current_active_admin)]
