import logging

from typing import Annotated, AsyncGenerator

from fastapi import Depends, Query, Request
from pydantic import BaseModel

from src.exceptions import NotAdminHTTPException, NotAuthenticatedHTTPException
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
    if not token:
        logging.error("Ошибка получения токена: пользователь не аутентифицирован")
        raise NotAuthenticatedHTTPException
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


async def get_current_user(db: DBDep, token: str = Depends(get_token)) -> User | None:
    user_id = get_current_user_id(token)
    user = await AuthService(db).get_one_or_none_user(user_id=user_id)
    return user


UserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        logging.error("Ошибка доступа: пользователь не администратор")
        raise NotAdminHTTPException
    return current_user


AdminDep = Annotated[User, Depends(get_current_active_admin)]
