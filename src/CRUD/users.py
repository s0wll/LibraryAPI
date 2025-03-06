from src.CRUD.base import BaseCRUD
from src.models.users import UsersOrm
from src.CRUD.mappers.mappers import UserDataMapper


class UsersCRUD(BaseCRUD):
    model = UsersOrm
    mapper = UserDataMapper