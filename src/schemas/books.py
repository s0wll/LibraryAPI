from datetime import date

from pydantic import BaseModel

from src.schemas.authors import Author


class BookAddRequest(BaseModel):
    title: str
    description: str
    publication_date: date
    genre: str
    quantity: int
    authors_ids: list[int] | None = []


class BookAdd(BaseModel):
    title: str
    description: str
    publication_date: date
    genre: str
    quantity: int


class BookPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    publication_date: date | None = None
    genre: str | None = None
    quantity: int | None = None
    authors_ids: list[int] | None = []


class BookPatch(BaseModel):
    title: str | None = None
    description: str | None = None
    publication_date: date | None = None
    genre: str | None = None
    quantity: int | None = None


class Book(BookAdd):
    id: int


class BookWithRels(Book):
    authors: list[Author]


class BookAuthorAdd(BaseModel):
    book_id: int
    author_id: int


class BookAuthor(BookAuthorAdd):
    id: int
