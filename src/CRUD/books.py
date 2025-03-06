from src.CRUD.base import BaseCRUD
from src.models.books import BooksOrm
from src.CRUD.mappers.mappers import BookDataMapper


class AuthorsCRUD(BaseCRUD):
    model = BooksOrm
    mapper = BookDataMapper