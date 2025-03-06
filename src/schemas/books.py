from pydantic import BaseModel


class BookAddRequest(BaseModel):
    title: str
    description: str
    publication_date: str
    genre: str
    quantity: int
    authors_ids: list[int] | None = []


class BookAdd(BaseModel):
    title: str
    description: str
    publication_date: str
    genre: str
    quantity: int


class Book(BookAdd):
    id: int
