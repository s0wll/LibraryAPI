import logging

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from schemas.users import User
from src.exceptions import ObjectNotFoundException
from src.CRUD.base import BaseCRUD
from src.models.users import UsersOrm
from src.CRUD.mappers.mappers import UserDataMapper, UserWithHashedPasswordDataMapper


class UsersCRUD(BaseCRUD):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> User:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound as exc:
            logging.error(f"Ошибка получения данных пользователя из БД, тип ошибки: {type(exc)=}")
            raise ObjectNotFoundException
        return UserWithHashedPasswordDataMapper.map_to_domain_entity(model)
