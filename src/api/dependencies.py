from typing import Annotated

from fastapi import Depends, Request

from services.auth import AuthService
from src.utils.db_manager import DBManager
from src.database import async_session_maker


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    return token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    return data["user_id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
