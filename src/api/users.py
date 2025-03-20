import logging

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException
from src.api.dependencies import AdminDep, UserDep, DBDep
from src.services.users import UsersService
from src.schemas.users import UserIsAdminRequest, UserPatch


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
@cache(expire=10)
async def get_all_users(admin_check: AdminDep, db: DBDep):
    logging.info("Получение списка всех пользователей /get_all_users")
    users = await UsersService(db).get_all_users()
    logging.info("Успешное получение списка всех пользоваталей")
    return users


@router.get("/{user_id}")
@cache(expire=10)
async def get_current_user_role(user: UserDep, db: DBDep):
    logging.info("Получение роли текущего пользователя /get_current_user_role")
    current_user_role = await UsersService(db).get_current_user_role(user.id)
    logging.info("Успешное получение роли текущего пользователя")
    return current_user_role


@router.put("/{user_id}/role")
async def assign_user_role(
    admin_check: AdminDep, user_id: int, db: DBDep, user_data: UserIsAdminRequest
):
    logging.info("Назначение роли пользователю /assign_user_role")
    await UsersService(db).assign_user_role(user_id, user_data)
    logging.info("Успешное назначение роли пользователю")
    return {"status": "OK"}


@router.patch("/{user_id}")
async def update_user(user: UserDep, db: DBDep, user_data: UserPatch):
    logging.info("Обновление данных пользователя /update_user")
    try:
        await UsersService(db).update_user(user.id, user_data)
        logging.info("Успешное обновление данных пользователя")
    except UserAlreadyExistsException:
        logging.error("Ошибка обновления данных пользователя: пользователь уже существует")
        raise UserAlreadyExistsHTTPException
    return {"status": "OK"}
