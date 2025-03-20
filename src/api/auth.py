import logging

from fastapi import APIRouter, Response
from fastapi import BackgroundTasks

from src.exceptions import IncorrectPasswordException, IncorrectPasswordHTTPException, UserAlreadyExistsException, UserAlreadyExistsHTTPException, UserEmailNotFoundHTTPException, UserNotFoundException
from src.api.dependencies import UserDep, DBDep
from src.services.auth import AuthService
from src.schemas.users import UserAddRequest, UserLoginRequest


router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register")
async def register_user(data: UserAddRequest, db: DBDep, background_tasks: BackgroundTasks):
    logging.info("Регистрация пользователя /register_user")
    try:
        await AuthService(db).register_user(data, background_tasks)
        logging.info("Успешная регистрация пользователя")
    except UserAlreadyExistsException:
        logging.error("Ошибка регистрации пользователя, пользователь уже существует")
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserLoginRequest,
    response: Response,
    db: DBDep,
):
    logging.info("Авторизация пользователя /login_user")
    try:
        access_token = await AuthService(db).login_user(data)
        logging.info("Успешная авторизация пользователя")
    except UserNotFoundException:
        logging.error("Ошибка авторизации пользователя, пользователь не найден")
        raise UserEmailNotFoundHTTPException
    except IncorrectPasswordException:
        logging.error("Ошибка авторизации пользователя, неверный пароль")
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(user: UserDep, db: DBDep):
    logging.info("Получение данных о текущем пользователе /get_me")
    user = await AuthService(db).get_one_or_none_user(user.id)
    logging.info("Успешное получение данных о текущем пользователе")
    return user


@router.post("/logout")
async def logout_user(response: Response):
    logging.info("Выход пользователя /logout_user")
    await AuthService().logout_user(response)
    logging.info("Успешный выход пользователя")
    return {"status": "OK"}