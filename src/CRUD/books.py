from src.CRUD.base import BaseCRUD
from src.models.books import BooksAuthorsOrm, BooksOrm
from src.CRUD.mappers.mappers import BookAuthorDataMapper, BookDataMapper


class BooksCRUD(BaseCRUD):
    model = BooksOrm
    mapper = BookDataMapper


class BooksAuthorsCRUD(BaseCRUD):
    model = BooksAuthorsOrm
    mapper = BookAuthorDataMapper