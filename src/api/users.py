from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import AdminDep, UserDep, DBDep
from src.services.users import UsersService
from src.schemas.users import UserIsAdminRequest, UserPatch


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("")
@cache(expire=10)
async def get_all_users(admin_check: AdminDep, db: DBDep):
    return await UsersService(db).get_all_users()


@router.get("/{user_id}")
@cache(expire=10)
async def get_current_user_role(user: UserDep, db: DBDep):
    return await UsersService(db).get_current_user_role(user.id)


@router.post("/{user_id}")
async def assign_current_user_role(admin_check: AdminDep, user: UserDep, db: DBDep, user_data: UserIsAdminRequest):
    await UsersService(db).assign_user_role(user.id, user_data)
    return {"status": "OK"}


@router.patch("/{user_id}")
async def update_user(user: UserDep, db: DBDep, user_data: UserPatch):
    await UsersService(db).update_user(user.id, user_data)
    return {"status": "OK"}
