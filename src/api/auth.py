from fastapi import APIRouter, Response

from src.api.dependencies import UserIdDep, DBDep
from src.services.auth import AuthService
from src.schemas.users import UserAddRequest


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    await AuthService(db).register_user(data)
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserAddRequest,
    response: Response,
    db: DBDep,
):
    access_token = await AuthService(db).login_user(data)
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout_user(response: Response):
    await AuthService().logout_user(response)
    return {"status": "OK"}