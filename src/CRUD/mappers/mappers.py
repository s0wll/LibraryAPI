from src.CRUD.mappers.base import DataMapper
from src.models.authors import AuthorsOrm
from src.schemas.authors import Author
from src.models.books import BooksAuthorsOrm, BooksOrm
from src.schemas.books import Book, BookAuthor
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashedPassword


class AuthorDataMapper(DataMapper):
    db_model = AuthorsOrm
    schema = Author


class BookDataMapper(DataMapper):
    db_model = BooksOrm
    schema = Book


class BookAuthorDataMapper(DataMapper):
    db_model = BooksAuthorsOrm
    schema = BookAuthor


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class UserWithHashedPasswordDataMapper(DataMapper):
    db_model = UsersOrm
    schema = UserWithHashedPassword