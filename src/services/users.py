from typing import Any

from pydantic import BaseModel

from src.schemas.users import UserIsAdminRequest, UserPatch
from src.services.base import BaseService


class UsersService(BaseService):
    async def get_all_users(self) -> list[BaseModel | None]:
        return await self.db.users.get_all()

    async def get_current_user_role(self, user_id: int) -> str:
        current_user = await self.db.users.get_one_or_none(id=user_id)
        if not current_user.is_admin:
            return "Вы не являетесь администратором"
        else:
            return "Вы являетесь администратором"
    
    async def assign_user_role(self, user_id: int, user_data: UserIsAdminRequest) -> None:
        await self.db.users.update(id=user_id, data=user_data)
        await self.db.commit()

    async def update_user(self, user_id: int, user_data: UserPatch) -> None:
        await self.db.users.update(id=user_id, data=user_data, exclude_unset=True)
        await self.db.commit()
