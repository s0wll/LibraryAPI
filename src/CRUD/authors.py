from src.CRUD.base import BaseCRUD
from src.models.authors import AuthorsOrm
from src.CRUD.mappers.mappers import AuthorDataMapper


class AuthorsCRUD(BaseCRUD):
    model = AuthorsOrm
    mapper = AuthorDataMapper
