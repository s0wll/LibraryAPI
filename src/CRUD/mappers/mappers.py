from src.CRUD.mappers.base import DataMapper
from src.models.authors import AuthorsOrm
from src.schemas.authors import Author
from src.models.books import BooksOrm
from src.schemas.books import Book
from src.models.users import UsersOrm
from src.schemas.users import User


class AuthorDataMapper(DataMapper):
    db_model = AuthorsOrm
    schema = Author


class BookDataMapper(DataMapper):
    db_model = BooksOrm
    schema = Book


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User