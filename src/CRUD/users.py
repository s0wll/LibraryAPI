from typing import Any

from pydantic import BaseModel, EmailStr
from sqlalchemy import select

from src.CRUD.base import BaseCRUD
from src.models.users import UsersOrm
from src.CRUD.mappers.mappers import UserDataMapper, UserWithHashedPasswordDataMapper


class UsersCRUD(BaseCRUD):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> BaseModel | Any:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
    