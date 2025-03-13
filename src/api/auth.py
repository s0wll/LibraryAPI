from fastapi import APIRouter, Response

from src.exceptions import IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, UserEmailNotFoundHTTPException, UserNotFoundException
from src.api.dependencies import UserDep, DBDep
from src.services.auth import AuthService
from src.schemas.users import UserAddRequest, UserLoginRequest


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserLoginRequest,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except UserNotFoundException:
        raise UserEmailNotFoundHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user: UserDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user.id)


@router.post("/logout")
async def logout_user(response: Response):
    await AuthService().logout_user(response)
    return {"status": "OK"}